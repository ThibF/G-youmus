import json
import logging
from enum import Enum

import boto3 as boto3

from config import config
from fifo_parser.facebookmessage import FacebookMessage
from fifo_parser.googlemessage import GoogleMessage


class Source(Enum):
    GOOGLE = 1
    FACEBOOK = 2


def is_payload_from(payload):
    if type(payload) == str:
        payload = json.loads(payload)
    if type(payload) == str:
        payload = json.loads(payload)
    try:
        sender_id = payload["entry"][0]["messaging"][0]["sender"]["id"]
        return Source.FACEBOOK
    except KeyError as e:
        return Source.GOOGLE


class MessagesListener:
    sqs = None

    def __init__(self):
        logging.info("Service starting")
        self.sqs = boto3.resource('sqs', aws_access_key_id=config["access_key"],
                                  aws_secret_access_key=config["secret_access_key"], region_name=config["region_name"],
                                  endpoint_url=config["endpoint_url"])
        self.queue = self.sqs.get_queue_by_name(QueueName=config["QueueName"])
        logging.info("sqs successfully accessed")

    def receive_messages(self):
        logging.info("Waiting for message")
        logging.getLogger().setLevel(level=logging.ERROR)
        for msg in self.queue.receive_messages():
            logging.getLogger().setLevel(level=logging.INFO)
            logging.info("Received =" + str(msg.body))
            msg.delete()
            return MessagesListener.wrap_raw_msg(msg)

    @staticmethod
    def wrap_raw_msg(msg):
        source = is_payload_from(msg.body)
        if source == Source.FACEBOOK:
            msg_wrapper = FacebookMessage(msg.body)
            return msg_wrapper
        elif source == Source.GOOGLE:
            msg_wrapper = GoogleMessage(msg.body)
            return msg_wrapper
        else:
            raise NotImplementedError
