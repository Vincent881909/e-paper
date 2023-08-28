import os
from PIL import Image, ImageFont, ImageEnhance, ImageDraw
import matplotlib.pyplot as plt
from logger import logger

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'assets')

try:
    VARELA_ROUND_18 = ImageFont.truetype(os.path.join(ASSETS_DIR, 'Varela_Round.ttf'), 18) 
    IBM_24 = ImageFont.truetype(os.path.join(ASSETS_DIR, 'IBM.ttf'), 24)
    IBM_18 = ImageFont.truetype(os.path.join(ASSETS_DIR, 'IBM.ttf'), 18) 
except IOError as e:
    logger.error(f"Font loading error: {e}")


def create_plot(exchange_rates, dates):
    try:
        fig, ax = plt.subplots(dpi=300)
        ax.plot(dates, exchange_rates, marker='o', linestyle='-', linewidth=4)
        ax.axis('off')
        plt.grid(False)
        plt.savefig('currency_trend.png', dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    except Exception as e:
        logger.error(f"Error during plotting: {e}")


def conduct_image_processing():
    try:
        img = Image.open('currency_trend.png').convert('L')
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.convert('1', dither=Image.NONE)
        img = img.resize((200, 65))
        img.save('currency_trend.bmp')
    except FileNotFoundError:
        logger.error("currency_trend.png not found for image processing.")
    except Exception as e:
        logger.error(f"Error during image processing: {e}")


def init_canvas(height, width):
    Himage = Image.new('1', (height, width), 255)  
    draw = ImageDraw.Draw(Himage)

    return draw, Himage


def currency_labels(draw_obj, base_currency, target_currency):
    draw_obj.rectangle((0, 0, 75, 126), fill=0)
    draw_obj.text((15, 23), base_currency, font=IBM_24, fill=1)
    draw_obj.text((15, 72), target_currency, font=IBM_24, fill=1)


def change_in_rate(value, draw_object):
    sign = ''
    if (value >= 0): sign = '+'
    draw_object.text((205, 106), f'{sign}{value} %', font=VARELA_ROUND_18, fill=0)


def exchange_rate(draw_object, change_in_rate, exchange_rate, target_symbol):
    target_symbol = decode_symbol(target_symbol)
    draw_object.text((105, 104), f'{str(exchange_rate)} {target_symbol}', font=IBM_18, fill=0)


def date_of_conversion(draw_obj, date):
    draw_obj.text((105, 10), date, font = IBM_18, fill = 0)


def trend_graph(currency_trend, image_obj):
    values = currency_trend[0]
    dates = currency_trend[1]
    create_plot(values,dates)
    conduct_image_processing()
    trend_img = Image.open('currency_trend.bmp')
    image_obj.paste(trend_img, (85,36))
    delete_png_bmp_files()


def delete_png_bmp_files():
    current_directory = os.getcwd()

    for filename in os.listdir(current_directory):
        if filename.endswith('.png') or filename.endswith('.bmp'):
            try:
                os.remove(os.path.join(current_directory, filename))
                logger.debug(f"Deleted: {filename}")
            except PermissionError:
                logger.error(f"Permission denied: Could not delete {filename}")
            except FileNotFoundError:
                logger.error(f"File not found: {filename}")


def decode_symbol(s):
    return bytes(s, 'ascii').decode('unicode-escape')
