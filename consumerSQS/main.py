import boto3
import logging
from config import config
import answer
import json
import time
import librarian
import consumer
import messageFacebook
import messageGoogle
from enum import Enum
import os
from config import config
import sys
import traceback

class Source(Enum):
     GOOGLE = 1
     FACEBOOK = 2

def isPayloadFrom(payload):
    if type(payload) == str :
            payload = json.loads(payload)
    if type(payload) == str :
        payload = json.loads(payload) 
    try :
        sender_id = payload["entry"][0]["messaging"][0]["sender"]["id"]
        return Source.FACEBOOK
    except KeyError as e:
        return Source.GOOGLE

    
if not os.path.exists(config["library_path"]):
    logging.critical("Library folder doesn't exist")
    sys.exit("Library folder doesn't exist")
    


logging.info("Service starting")
sqs = boto3.resource('sqs',aws_access_key_id = config["access_key"], aws_secret_access_key=config["secret_access_key"], region_name="us-west-2", endpoint_url="https://sqs.us-west-2.amazonaws.com/731910755973/MessagesYouMus.fifo")
logging.info("sqs succesfully accessed")
logging.info("Waiting for message")
while True:
    queue = sqs.get_queue_by_name(QueueName='MessagesYouMus.fifo')
    for msg in queue.receive_messages():
        logging.getLogger().setLevel(level=logging.DEBUG)
        logging.debug("Received ="+str(msg.body))
        source = isPayloadFrom(msg.body)
        try:
            if source == Source.FACEBOOK :
                msg_wrapper = messageFacebook.MessageFacebook(msg.body)
                msg.delete()
                status = consumer.work(msg_wrapper)
            elif source == Source.GOOGLE :
                msg_wrapper = messageGoogle.MessageGoogle(msg.body)
                msg.delete()
                status = consumer.work(msg_wrapper)
            else:
                pass 
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            logging.error("Show must go on\n")
        logging.getLogger().setLevel(level=logging.ERROR)
    time.sleep(0.2)
