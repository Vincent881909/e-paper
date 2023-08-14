import schedule
import time
from datetime import datetime
import os, sys
from main import main_script 

# Directories
LIB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

from logger import logger

def run_task():
    try:
        logger.info(f"Running task at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        main_script()
    except Exception as e:
        logger.error(f"Error while executing the task: {e}")

if __name__ == "__main__":
    run_task()

    schedule.every().day.at("00:00").do(run_task)

    while True:
        schedule.run_pending()
        time.sleep(1)
