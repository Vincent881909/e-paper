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
import datetime
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
    return f"{conversion_rate} {currency_symbols[target_currency]}"

def date_of_conversion():
    date_object = datetime.datetime.fromtimestamp(TIME_STAMP)
    date = date_object.strftime('%a %d %B %Y')
    return f"{date}"

logging.basicConfig(level=logging.DEBUG)



API_KEY1 = '8137072dc2801b3010638855a4faefbb'
base = 'EUR'
symbols = 'ZAR'

end_date = datetime.date.today()

start_date = end_date - datetime.timedelta(weeks=1)

num_days = (end_date - start_date).days

dates = []
exchange_rates = []

for day in range(num_days):
    current_date = start_date + datetime.timedelta(days=day)
    URL = f'http://api.exchangeratesapi.io/v1/{current_date}?access_key={API_KEY1}&base={base}&symbols={symbols}'

    request = requests.get(URL)
    request.raise_for_status() 
    data = request.json()
    print("DATA=======\n")
    print(data) 
    dates.append(current_date)
    exchange_rates.append(data['rates'][symbols])



#Plotting the trend and saving it
fig, ax = plt.subplots(dpi=300)  # Set DPI at creation time
ax.plot(dates, exchange_rates, marker='o')
ax.axis('off')
plt.grid(False)

plt.savefig('exchange_rate.png', dpi=300, bbox_inches='tight', pad_inches=0)
img = Image.open('exchange_rate.png').convert('L')  # Convert to grayscale
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)
img = img.convert('1', dither=Image.NONE)
img = img.resize((200, 65))
img.save('exchange_rate.bmp')


while True:

    try:
        epd = epd2in9b_V3.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        time.sleep(1)
         
        Varela_round = ImageFont.truetype(os.path.join(picdir, 'Varela_Round.ttf'), 18) 
        IBM_24 = ImageFont.truetype(os.path.join(picdir, 'IBM.ttf'), 24)
        IBM_18 = ImageFont.truetype(os.path.join(picdir, 'IBM.ttf'), 18) 
        
        black_image = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        red_image = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red  
        draw_black = ImageDraw.Draw(black_image)
        draw_red = ImageDraw.Draw(red_image)

        #Left Hand Side View
        draw_black.rectangle((0, 0,75, 126), fill = 0)
        draw_black.text((15, 23), 'EUR', font = IBM_24, fill = 1)
        draw_black.text((15, 72), 'ZAR', font = IBM_24, fill = 1)

        #Conversion Rate
        draw_red.text((145, 104), get_conversion('ZAR'), font = IBM_18, fill = 0)

        #Conversion Time
        draw_black.text((105, 10), date_of_conversion(), font = IBM_18, fill = 0)

        #Currency Trend
        newimage = Image.open('exchange_rate.bmp')
        black_image.paste(newimage, (85,36))

        epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image)) 
  
        #time.sleep(86400) # Upate every 24h 
        #time.sleep(43200) # Upate every 12h 
        time.sleep(21600) # Upate every 6h 
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in9b_V3.epdconfig.module_exit()
        exit()
