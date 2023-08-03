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
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance, ImageFilter
import datetime



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



API_KEY1 = '8137072dc2801b3010638855a4faefbb'
base = 'EUR'
symbols = 'ZAR'

# Today's date
end_date = datetime.date.today()

# Starting date (4 weeks ago)
start_date = end_date - datetime.timedelta(weeks=3)

# Number of days between start and end date
num_days = (end_date - start_date).days

# Lists to store dates and exchange rates
dates = []
exchange_rates = []

# Loop through the past 28 days (4 weeks)
for day in range(num_days):
    # Calculate the date for this iteration
    current_date = start_date + datetime.timedelta(days=day)
    
    # Create the URL for this date
    URL = f'http://api.exchangeratesapi.io/v1/{current_date}?access_key={API_KEY1}&base={base}&symbols={symbols}'
    
    # Make the request
    request = requests.get(URL)
    request.raise_for_status()  
    data = request.json()

    # Add the date and exchange rate to our lists
    dates.append(current_date)
    exchange_rates.append(data['rates'][symbols])




# Create a plot of exchange rates over time
fig, ax = plt.subplots(dpi=300)  # Set DPI at creation time
ax.plot(dates, exchange_rates, marker='o')

# Hide axes, labels, and title
ax.axis('off')

plt.grid(False)

# Save the figure as a grayscale PNG with increased DPI
plt.savefig('exchange_rate.png', dpi=300, bbox_inches='tight', pad_inches=0)

# Open the image file
img = Image.open('exchange_rate.png').convert('L')  # Convert to grayscale

# Enhance contrast to prepare for binary conversion
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)

# Binarize the image using Floyd-Steinberg dithering
img = img.convert('1', dither=Image.NONE)

# Resize the image to the final size
img = img.resize((296, 98))

# Save the binary black-and-white, resized image as a BMP
img.save('exchange_rate.bmp')


while True:

    try:
        epd = epd2in9b_V3.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        time.sleep(1)
        
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        
        #HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        #HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red  
        #drawblack = ImageDraw.Draw(HBlackimage)
        #drawry = ImageDraw.Draw(HRYimage)
        #drawblack.text((60, 0), 'Currency Tracker', font = font18, fill = 0)

        logging.info("4.read bmp file on window")
        blackimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        redimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126    
        newimage = Image.open('exchange_rate.bmp')
        blackimage1.paste(newimage, (0,10))
        epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

    
        #drawblack.text((10, 10), get_conversion('ZAR'), font = font18, fill = 0)
        #drawblack.text((10, 40), get_conversion('CAD'), font = font18, fill = 0)
        #drawblack.text((10, 100), date_of_conversion(), font = font18, fill = 0)
  
        #time.sleep(86400) # Upate every 24h 
        #time.sleep(43200) # Upate every 12h 
        time.sleep(21600) # Upate every 6h 
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in9b_V3.epdconfig.module_exit()
        exit()
