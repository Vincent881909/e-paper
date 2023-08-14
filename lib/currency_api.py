import os
import datetime
import requests
import redis
import json
from logger import logger

API_KEY = os.environ.get('CURRENCY_API_KEY')
if not API_KEY: logger.error("CURRENCY_API_KEY environment variable not found!")

BASE_CURRENCY = "EUR" # Default Value
TARGET_CURRENCY = "ZAR" # Default Value
TREND_IN_WEEKS = 4 # Default Value
CURRENCY_SYMBOLS = {
    'ZAR': '\u0052',  # South African Rand 
    'CAD': '\u0024',  # Canadian Dollar
    'EUR': '\u20AC',  # Euro
    'USD': '\u0024'   # United States Dollar
}

REDIS_CLIENT = redis.Redis(host='localhost', port=6379, db=0)

def timestamp_to_date(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime('%a %d %B %Y')

def get_exchange_rate(date):
    try:
        date = date.strftime('%Y-%m-%d')
        client_key = f'{BASE_CURRENCY}:{TARGET_CURRENCY}:{date}'
        data = REDIS_CLIENT.get(client_key)

        if data is None:
            logger.debug(f'Client Key: {client_key} does not exist. API call initiated.')
            url = f'http://api.exchangeratesapi.io/v1/{date}?access_key={API_KEY}&base={BASE_CURRENCY}&symbols={TARGET_CURRENCY}'
            
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            
            if 'rates' not in data or TARGET_CURRENCY not in data['rates']:
                logger.error(f"Unexpected API response structure: {data}")
                return None, None

            seconds_in_six_months = 6 * 30 * 24 * 60 * 60
            REDIS_CLIENT.setex(client_key, seconds_in_six_months, json.dumps(data))
            
        else:
            logger.debug(f'Client Key: {client_key} exists. Caching used.')
            data = json.loads(data)

        exchange_rate = data['rates'][TARGET_CURRENCY]
        timestamp = data['timestamp']
        date = timestamp_to_date(timestamp)

        return round(exchange_rate, 2), date

    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred when fetching data for {date}: {e}")
        return None, None
    except requests.RequestException as e:
        logger.error(f"Network error occurred: {e}")
        return None, None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        return None, None
    except redis.RedisError as e:
        logger.error(f"Redis error: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None, None


def fetch_currency_trend(weeks_duration):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(weeks=weeks_duration)
    num_days = (end_date - start_date).days
    dates = []
    exchange_rates = []

    for day in range(num_days):
        current_date = start_date + datetime.timedelta(days=day)
        exchange_rates.append(get_exchange_rate(current_date)[0])
        dates.append(current_date)

    return exchange_rates, dates


def trend_value(weeks_duration):
    todays_date = datetime.date.today()
    start_date = todays_date - datetime.timedelta(weeks=weeks_duration)
    old_rate = get_exchange_rate(start_date)[0]
    todays_rate = get_exchange_rate(todays_date)[0]
    trend = ((todays_rate - old_rate) / old_rate) * 100
    return round(trend,2)

def seconds_until_midnight():
    now = datetime.datetime.now()
    midnight = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time())
    return int((midnight - now).total_seconds())

