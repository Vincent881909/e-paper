import os
import datetime
import requests
import redis
import json

API_KEY = os.environ.get('CURRENCY_API_KEY')
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
    date = date.strftime('%Y-%m-%d')

    client_key = f'{BASE_CURRENCY}:{TARGET_CURRENCY}:{date}'
    data = REDIS_CLIENT.get(client_key)

    if data is None:
        print(f'Client Key: {client_key} does not exist. API call initiated.')
        url = f'http://api.exchangeratesapi.io/v1/{date}?access_key={API_KEY}&base={BASE_CURRENCY}&symbols={TARGET_CURRENCY}'
        request = requests.get(url)
        request.raise_for_status()
        data = request.json()
        seconds_in_six_months = 6 * 30 * 24 * 60 * 60
        REDIS_CLIENT.setex(client_key, seconds_in_six_months, json.dumps(data))
    else:
        print(f'Client Key: {client_key} exists. Caching used.')
        data = json.loads(data)

    exchange_rate = data['rates'][TARGET_CURRENCY]
    timestamp = data['timestamp']
    date = timestamp_to_date(timestamp)
    return round(exchange_rate,2), date


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

