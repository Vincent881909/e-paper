import os
from PIL import Image, ImageFont, ImageEnhance, ImageDraw
import matplotlib.pyplot as plt

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'assets')

VARELA_ROUND_18 = ImageFont.truetype(os.path.join(ASSETS_DIR, 'Varela_Round.ttf'), 18) 
IBM_24 = ImageFont.truetype(os.path.join(ASSETS_DIR, 'IBM.ttf'), 24)
IBM_18 = ImageFont.truetype(os.path.join(ASSETS_DIR, 'IBM.ttf'), 18) 

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


def init_canvas(height, width):
    black_image = Image.new('1', (height, width), 255) 
    red_image = Image.new('1', (height, width), 255)
    draw_black = ImageDraw.Draw(black_image)
    draw_red = ImageDraw.Draw(red_image)

    return draw_black,draw_red,black_image,red_image


def currency_labels(draw_obj, base_currency, target_currency):
    draw_obj.rectangle((0, 0, 75, 126), fill=0)
    draw_obj.text((15, 23), base_currency, font=IBM_24, fill=1)
    draw_obj.text((15, 72), target_currency, font=IBM_24, fill=1)

def change_in_rate(value, draw_object):
    sign = ''
    if (value >= 0): sign = '+'
    draw_object.text((205, 106), f'{sign}{value} %', font=VARELA_ROUND_18, fill=0)


def exchange_rate(draw_obj_black, draw_obj_red, change_in_rate, exchange_rate, target_symbol):
    draw_obj = draw_obj_black
    if(change_in_rate) <= 0: draw_obj = draw_obj_red
    draw_obj.text((105, 104), f'{str(exchange_rate)} {target_symbol}', font=IBM_18, fill=0)


def date_of_conversion(draw_obj, date):
    draw_obj.text((105, 10), date, font = IBM_18, fill = 0)


def trend_graph(currency_trend, image_obj):
    values = currency_trend[0]
    dates = currency_trend[1]
    create_plot(values,dates)
    conduct_image_processing()
    trend_img = Image.open('currency_trend.bmp')
    image_obj.paste(trend_img, (85,36))
