from flask import Flask, render_template, request, redirect, url_for
import configparser
import os

app = Flask(__name__)

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'config.cfg')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        base_currency = request.form['base_currency']
        target_currency = request.form['target_currency']
        
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        
        config['DEFAULT']['BASE_CURRENCY'] = base_currency
        config['DEFAULT']['TARGET_CURRENCY'] = target_currency

        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

        # Redirect to the same page after saving configuration to show updated values
        return redirect(url_for('index'))
    else:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        base_currency = config['DEFAULT']['BASE_CURRENCY']
        target_currency = config['DEFAULT']['TARGET_CURRENCY']

        return render_template('index.html', base_currency=base_currency, target_currency=target_currency)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
