import requests
import logging

import os
from dotenv import load_dotenv
load_dotenv()

CHAPORT_API_KEY = os.getenv("CHAPORT_API_KEY")
CHAPORT_API_URL = "https://app.chaport.com/api/v1/messages"
OperatorID = '620d7da500ae61646bcf9011'


def send_response_to_chaport(visitor_id, message_text):

    if(message_text ==''):
        return None
    payload = {
        "visitorId": visitor_id,
        "chatEvent": {
            "type": "operator-message",
            "params": {
                "text": message_text,
                "operatorId": OperatorID
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {CHAPORT_API_KEY}",
        "Content-Type": "application/json",
        'Accept': 'application/json'
    }

    try:
        response = requests.post(CHAPORT_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Message sent to visitor ID {visitor_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logging.error(f"Response content: {e.response.text}")
        return None
if __name__ == "__main__":
    visitor_id = "67db74c36679c4267a1c2af1"
    response_text = "Hello a bot will answer in a bit"
    send_response_to_chaport(visitor_id, response_text)
