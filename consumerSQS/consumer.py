import boto3
import logging
from config import config
import answer
import json
import time
import librarian

def work(message):
    message = json.loads(message)
    print(type(message))
    print(message)
    return sendToManager(message)

def sendToManager(message):
    um = librarian.User_manager(message["entry"][0]["messaging"][0]["sender"]["id"])
    um.user_event("MESSAGE",str(message["entry"][0]["messaging"][0]["message"]["text"]))
    return True

def parrot_work(message):
    try :
        msgToSend = "I ear your request :"+str(message["entry"][0]["messaging"][0]["message"]["text"])
        idReceiver = message["entry"][0]["messaging"][0]["sender"]["id"]
        print (idReceiver+":"+msgToSend)
        answer.send_message(msgToSend,idReceiver)
        answer.send_message("I will",idReceiver)
        return True
    except Exception as e:
        print(e)
        return False

sqs = boto3.resource('sqs',aws_access_key_id = config["access_key"], aws_secret_access_key=config["secret_access_key"], region_name="us-west-2", endpoint_url="https://sqs.us-west-2.amazonaws.com/731910755973/MessagesYouMus.fifo")
while True:
    queue = sqs.get_queue_by_name(QueueName='MessagesYouMus.fifo')
    for msg in queue.receive_messages():
        status = work(json.loads(msg.body))
        if status:
            msg.delete()
        else:
            msg.delete()
    print("no msg, going to sleep")
    time.sleep(3)


