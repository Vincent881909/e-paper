#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os
import sys
import requests
import datetime
import time
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import matplotlib.pyplot as plt

# Directories
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'assets')
LIB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

from waveshare_epd import epd2in9b_V3

API_KEY = os.environ.get('CURRENCY_API_KEY')
BASE_CURRENCY = "EUR"
TARGET_CURRENCY = "ZAR"
TREND_IN_WEEKS = 4
CURRENCY_SYMBOLS = {
    'ZAR': '\u0052',  # South African Rand 
    'CAD': '\u0024',  # Canadian Dollar
    'EUR': '\u20AC',  # Euro
    'USD': '\u0024'   # United States Dollar
}

VARELA_ROUND_18 = ImageFont.truetype(os.path.join(ASSETS_DIR, 'Varela_Round.ttf'), 18) 
IBM_24 = ImageFont.truetype(os.path.join(ASSETS_DIR, 'IBM.ttf'), 24)
IBM_18 = ImageFont.truetype(os.path.join(ASSETS_DIR, 'IBM.ttf'), 18) 

def timestamp_to_date(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime('%a %d %B %Y')


def get_exchange_rate(date):
    date = date.strftime('%Y-%m-%d')
    url = f'http://api.exchangeratesapi.io/v1/{date}?access_key={API_KEY}&base={BASE_CURRENCY}&symbols={TARGET_CURRENCY}'
    request = requests.get(url)
    request.raise_for_status()
    received_data = request.json()
    exchange_rate = received_data['rates'][TARGET_CURRENCY]
    timestamp = received_data['timestamp']
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


def create_plot(exchange_rates, dates):
    fig, ax = plt.subplots(dpi=300)  # Set DPI at creation time
    ax.plot(dates, exchange_rates, marker='o')
    ax.axis('off')
    plt.grid(False)
    plt.savefig('currency_trend.png', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig)


def conduct_image_processing():
    img = Image.open('currency_trend.png').convert('L')  # Convert to grayscale
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.convert('1', dither=Image.NONE)
    img = img.resize((200, 65))
    img.save('currency_trend.bmp')


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

if __name__ == "__main__":

    while True:

        try:
            epd = epd2in9b_V3.EPD()
            logging.basicConfig(level=logging.DEBUG)
            logging.info("Init and Clear")
            epd.init()
            epd.Clear()
            time.sleep(1)
            
            black_image = Image.new('1', (epd.height, epd.width), 255) 
            red_image = Image.new('1', (epd.height, epd.width), 255)
            draw_black = ImageDraw.Draw(black_image)
            draw_red = ImageDraw.Draw(red_image)

            draw_black.rectangle((0, 0,75, 126), fill = 0)
            draw_black.text((15, 23), BASE_CURRENCY, font = IBM_24, fill = 1)
            draw_black.text((15, 72), TARGET_CURRENCY, font = IBM_24, fill = 1)

            rate_trend_percentage = trend_value(TREND_IN_WEEKS)
            current_exchange_rate = get_exchange_rate(datetime.datetime.now())
    
            if rate_trend_percentage >= 0:
                trend_sign = '+'
                color = draw_black
            else:
                trend_sign = ''
                color = draw_red

            draw_black.text((205, 106), f'{trend_sign}{rate_trend_percentage} %', font=VARELA_ROUND_18, fill=0)
            color.text((105, 104), f'{str(current_exchange_rate[0])} {CURRENCY_SYMBOLS[TARGET_CURRENCY]}', font=IBM_18, fill=0)

            date_of_conversion = current_exchange_rate[1]
            draw_black.text((105, 10), date_of_conversion, font = IBM_18, fill = 0)

            currency_trend = fetch_currency_trend(TREND_IN_WEEKS)
            values = currency_trend[0]
            dates = currency_trend[1]
            create_plot(values,dates)
            conduct_image_processing()
            trend_img = Image.open('currency_trend.bmp')
            black_image.paste(trend_img, (85,36))

            epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image)) 
            time.sleep(seconds_until_midnight()) #Scrip updates every night at midnight
                
        except IOError as e:
            logging.info(e)
            
        except KeyboardInterrupt:    
            logging.info("ctrl + c:")
            epd2in9b_V3.epdconfig.module_exit()
            exit()
