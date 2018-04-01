import boto3
import logging
from config import config
import answer
import json
import time
import librarian
import consumer
import messageFacebook

logging.info("Service starting")
sqs = boto3.resource('sqs',aws_access_key_id = config["access_key"], aws_secret_access_key=config["secret_access_key"], region_name="us-west-2", endpoint_url="https://sqs.us-west-2.amazonaws.com/731910755973/MessagesYouMus.fifo")
logging.info("sqs succesfully accessed")
logging.info("Waiting for message")
while True:
    queue = sqs.get_queue_by_name(QueueName='MessagesYouMus.fifo')
    for msg in queue.receive_messages():
        msg_wrapper = MessageFacebook(msg.body)
        logging.debug("\nReceived ="+msg_wrapper.get_text())
        status = consumer.work(msg_wrapper)
        logging.debug("code returned by work:"+str(status))
        msg.delete()
    time.sleep(0.2)