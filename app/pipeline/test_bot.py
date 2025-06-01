import requests
import pandas as pd

from mode_selection import mode_selection
from dotenv import load_dotenv
import os
import time
import logging
load_dotenv()

API_TOKEN = os.getenv("CHAPORT_API_KEY")
BASE_URL = "https://app.chaport.com/api/v1/visitors"

delay =0.5

request_count = 0
def run_bot():
    global request_count
    print("running testbot")
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }

    data = get_request(BASE_URL, headers)
    if data == None:
        return
    ids = [item["id"] for item in data["result"]]


    df = pd.DataFrame(ids, columns=["ID"])



    last_visitor_messages = {
        "message": [""],
        "event index": [-1]
    }

    last_op_message = pd.DataFrame(columns=["message", "event index"])
    last_op_message.loc[0] = ["", -1]
    scanned_messages = []

    time.sleep(delay)
    for id_value in df["ID"]:
        url = f"https://app.chaport.com/api/v1/visitors/{id_value}/chats"
        last_chat = get_request(url, headers)
        if last_chat == None:
            continue
        events = last_chat['result']['events']
        last_msg_sent = ''
        sent_message = ''
        for e in range(len(events)):
            if(events[e]['type'] == 'visitor-message' or events[e]['type'] == 'operator-message' and events[e]['id'] not in scanned_messages):
                scanned_messages.append(events[e]['id'])
                if(events[e]['type'] == 'visitor-message'):
                    new_data = {
                        "message": events[e]['params']['text'],
                        "event index": e
                    }
                    last_visitor_messages["message"].append(new_data["message"])
                    last_visitor_messages["event index"].append(new_data["event index"])
                if(events[e]['type'] == 'operator-message'):
                    last_visitor_messages = {
                        "message": [""],
                        "event index": [-1]
                    }
                    last_op_message.iloc[0] = [events[e]['params']['text'], e]
                #print(events[e]['type'],": ", events[e]['params']['text'])

                sent_message = events[e]['params']['text']

        if(last_visitor_messages["event index"][-1]> last_op_message.iloc[0]['event index']):
            for msg in last_visitor_messages["message"]:
                mode_selection(msg, id_value)

        last_visitor_messages = {
            "message": [""],
            "event index": [-1]
        }
        last_op_message.loc[0] = ["", -1]
        time.sleep(delay)


logging.basicConfig(level=logging.INFO)

def get_request(url, headers, max_retries=1000, base_delay=2, timeout=10):
    global request_count
    attempt = 0
    delay = base_delay

    while attempt < max_retries:
        try:
            r = requests.get(url, params={}, headers=headers, timeout=timeout)
            r.raise_for_status()
            request_count += 1
            return r.json()
        except requests.exceptions.RequestException as e:
            logging.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            attempt += 1
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
            else:
                logging.error("All retries failed. Giving up.")
                return None

def count_request():
    global request_count
    request_count += 1
def get_request_count():
    return request_count

def get_recent_conversation():
    from datetime import datetime
    import pytz


    last_seen = '2025-05-06T06:53:43.155Z'

    utc_time = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S.%fZ")

    utc_time = pytz.utc.localize(utc_time)

    pst_timezone = pytz.timezone('US/Pacific')
    pst_time = utc_time.astimezone(pst_timezone)
    return pst_time

if __name__ == "__main__":
    run_bot()