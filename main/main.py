#!/usr/bin/python

import logging
import os
import sys
import datetime
import time

# Directories
LIB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

import epd2in9b_V3
import currency_api
import draw

if __name__ == "__main__":

    while True:

        try:
            epd = epd2in9b_V3.EPD()
            logging.basicConfig(level=logging.DEBUG)
            logging.info("Init and Clear")
            epd.init()
            epd.Clear()

            current_rate, conversion_date = currency_api.get_exchange_rate(datetime.datetime.now())
            currency_trend = currency_api.fetch_currency_trend(currency_api.TREND_IN_WEEKS)
            trend_percentage_change = currency_api.trend_value(currency_api.TREND_IN_WEEKS)

            draw_black,draw_red,black_image,red_image = draw.init_canvas(epd.height,epd.width)
            
            draw.currency_labels(draw_black,currency_api.BASE_CURRENCY,currency_api.TARGET_CURRENCY)
            draw.change_in_rate(trend_percentage_change,draw_black)
            draw.exchange_rate(draw_black,draw_red,trend_percentage_change,current_rate,currency_api.CURRENCY_SYMBOLS[currency_api.TARGET_CURRENCY])
            draw.date_of_conversion(draw_black,conversion_date)
            draw.trend_graph(currency_trend,black_image)
            epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image)) 

            time.sleep(currency_api.seconds_until_midnight()) #Scrip updates every night at midnight
                
        except IOError as e:
            logging.info(e)
            
        except KeyboardInterrupt:    
            logging.info("ctrl + c:")
            epd2in9b_V3.epdconfig.module_exit()
            exit()
