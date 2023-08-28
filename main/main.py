#!/usr/bin/python

import os
import sys
import datetime
import time
import configparser

# Directories
LIB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

import epd2in9_V2
import currency_api
import draw
from logger import logger

def main_script():
    try:
        
        epd = epd2in9_V2.EPD()
        logger.info("Init and Clear")
        epd.init()
        epd.Clear(0xFF)

        config,config_file_path = currency_api.get_config_object()
        config.read(config_file_path)

        current_rate, conversion_date = currency_api.get_exchange_rate(datetime.datetime.now())
        currency_trend = currency_api.fetch_currency_trend(int(config['DEFAULT']['TREND_IN_WEEKS']))
        trend_percentage_change = currency_api.trend_value(int(config['DEFAULT']['TREND_IN_WEEKS']))
        logger.info("Data has been fetched")

        draw_object,Himage = draw.init_canvas(epd.height,epd.width)
        draw.currency_labels(draw_object,config["DEFAULT"]["BASE_CURRENCY"],config["DEFAULT"]["TARGET_CURRENCY"])
        draw.change_in_rate(trend_percentage_change,draw_object)
        draw.exchange_rate(draw_object,trend_percentage_change,current_rate,config["CURRENCY_SYMBOLS"][config["DEFAULT"]["TARGET_CURRENCY"]])
        draw.date_of_conversion(draw_object,conversion_date)
        draw.trend_graph(currency_trend,Himage)
        epd.display(epd.getbuffer(Himage)) 
         
        epd.init()
        logger.info("Enter Sleep Mode")
        epd.sleep()
            
    except IOError as e:
        logger.info(e)
        
    except KeyboardInterrupt:    
        logger.info("ctrl + c:")
        epd2in9_V2.epdconfig.module_exit()
        exit()
