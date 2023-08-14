from flask import Flask, render_template, request, redirect, url_for
import configparser
import os, sys

# Directories
LIB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

MAIN_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'main')
if os.path.exists(MAIN_DIR):
    sys.path.append(MAIN_DIR)

from logger import logger
from main import main_script
import currency_api

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    config,config_file_path = currency_api.get_config_object()
    config.read(config_file_path)

    if request.method == 'POST':
        logger.debug("POST method recognized")
        base_currency = request.form['BASE_CURRENCY']
        target_currency = request.form['TARGET_CURRENCY']
        
        config['DEFAULT']['BASE_CURRENCY'] = base_currency
        config['DEFAULT']['TARGET_CURRENCY'] = target_currency

        with open(config_file_path, 'w') as configfile:
            config.write(configfile)

        #Reload main script to apply changes to e-paper
        main_script()

        # Redirect to the same page after saving configuration to show updated values
        return redirect(url_for('index'))
    else:
        logger.debug("GET method recognized")
        base_currency = config['DEFAULT']['BASE_CURRENCY']
        target_currency = config['DEFAULT']['TARGET_CURRENCY']

        return render_template('index.html', base_currency=base_currency, target_currency=target_currency)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

