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

import epd2in9b_V3
import currency_api
import draw
from logger import logger

def main_script():
    try:
        
        epd = epd2in9b_V3.EPD()
        logger.info("Init and Clear")
        epd.init()
        epd.Clear()

        config,config_file_path = currency_api.get_config_object()
        config.read(config_file_path)

        current_rate, conversion_date = currency_api.get_exchange_rate(datetime.datetime.now() - datetime.timedelta(days=1))
        currency_trend = currency_api.fetch_currency_trend(int(config['DEFAULT']['TREND_IN_WEEKS']))
        trend_percentage_change = currency_api.trend_value(int(config['DEFAULT']['TREND_IN_WEEKS']))
        logger.info("Data has been fetched")

        draw_black,draw_red,black_image,red_image = draw.init_canvas(epd.height,epd.width)
        draw.currency_labels(draw_black,config["DEFAULT"]["BASE_CURRENCY"],config["DEFAULT"]["TARGET_CURRENCY"])
        draw.change_in_rate(trend_percentage_change,draw_black)
        draw.exchange_rate(draw_black,draw_red,trend_percentage_change,current_rate,config["CURRENCY_SYMBOLS"][config["DEFAULT"]["TARGET_CURRENCY"]])
        draw.date_of_conversion(draw_black,conversion_date)
        draw.trend_graph(currency_trend,black_image)
        epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image)) 

        logger.info("Data has been displayed")
        logger.info("Script re-executed at midnight or until refreshed via web-gui")
            
    except IOError as e:
        logger.info(e)
        
    except KeyboardInterrupt:    
        logger.info("ctrl + c:")
        epd2in9b_V3.epdconfig.module_exit()
        exit()
