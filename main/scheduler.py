import schedule
import requests
import time
from datetime import datetime
import os,sys
import subprocess
from main import main_script 

# Directories
LIB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'web')
if os.path.exists(WEB_DIR):
    sys.path.append(WEB_DIR)

from logger import logger


def check_network_connection():
    url = "http://www.google.com"
    timeout = 5 
    
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            logger.info("Network connection established.")
            return True
    except requests.ConnectionError:
        pass
    return False


def run_task():
    while not check_network_connection():
        logger.error("Network connection not established. Retrying in 60 seconds...")
        time.sleep(60)

    try:
        logger.info(f"Running task at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        main_script()
    except Exception as e:
        logger.error(f"Error while executing the task: {e}")


if __name__ == "__main__":
    # Initial run
    run_task()

    logger.debug(os.path.join(WEB_DIR, "app.py"))
    result = subprocess.Popen(["python3", os.path.join(WEB_DIR, "app.py")])

    #Scheduled Task
    schedule.every().day.at("06:00").do(run_task)

    while True:
        schedule.run_pending()
        time.sleep(1)