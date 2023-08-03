#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import os
import sys

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image,ImageDraw,ImageFont
import requests
from datetime import timedelta, datetime
import time
import traceback
from waveshare_epd import epd2in9b_V3



# Setup Currecncy API
API_KEY = "60d868a310906f1923f9b632"
BASE_CURRENCY = "EUR"
TIME_STAMP = 0

currency_symbols = {
    'ZAR': '\u0052',  # South African Rand - U+0052
    'CAD': '\u0024',  # Canadian Dollar - U+0024
    'EUR': '\u20AC',  # Euro - U+20AC
}


def get_conversion(target_currency):
    global TIME_STAMP
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{BASE_CURRENCY}/{target_currency}'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    conversion_rate = data['conversion_rate']
    TIME_STAMP = data['time_last_update_unix']
    return f"1 {currency_symbols[BASE_CURRENCY]} equates to {conversion_rate} {currency_symbols[target_currency]}"

def date_of_conversion():
    date_object = datetime.fromtimestamp(TIME_STAMP)
    date = date_object.strftime('%d-%m-%Y')
    return f"Time of conversion: {date}"

logging.basicConfig(level=logging.DEBUG)

while True:

    try:
        epd = epd2in9b_V3.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        time.sleep(1)
        
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red  
        drawblack = ImageDraw.Draw(HBlackimage)
        drawry = ImageDraw.Draw(HRYimage)
        #drawblack.text((55, 0), 'Currency Tracker', font = font24, fill = 0)
        drawblack.text((10, 10), get_conversion('ZAR'), font = font18, fill = 0)
        drawblack.text((10, 40), get_conversion('CAD'), font = font18, fill = 0)
        drawblack.text((10, 100), date_of_conversion(), font = font18, fill = 0)

        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        epd.sleep()
        #time.sleep(86400) # Upate every 24h 
        #time.sleep(43200) # Upate every 12h 
        time.sleep(21600) # Upate every 6h 
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in9b_V3.epdconfig.module_exit()
        exit()
