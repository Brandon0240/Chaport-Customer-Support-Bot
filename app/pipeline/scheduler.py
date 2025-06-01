import schedule
import time
import logging
import atexit
from datetime import datetime

from test_bot import run_bot , get_request_count


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

start_time = datetime.now()

def log_total_runtime():
    end_time = datetime.now()
    total_runtime = end_time - start_time
    logging.info(f"Total run time: {total_runtime}")
    logging.info(f"Total Request: {get_request_count()}")
    logging.info(f"Request/sec: {logging.info(f"Request/sec: {get_request_count() / total_runtime.total_seconds():.2f}")}")

atexit.register(log_total_runtime)

def run_bot_continuously():

    run_bot()
    logging.info(f"Requests this run: {get_request_count()}")
schedule.every(1).seconds.do(run_bot_continuously)

if __name__ == "__main__":
    logging.info("Scheduler started.")
    try:
        while True:
            logging.info("Scheduler is running... waiting for the next task.")
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Scheduler interrupted by user.")
