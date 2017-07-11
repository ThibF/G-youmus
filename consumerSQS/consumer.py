import boto3
import logging
from config import config
import answer
import json
import time
import librarian

def work(message):
    try :
        message = json.loads(message)
    except Exception as e:
        print("lol info just")
    print(type(message))
    print(message)
    return sendToManager(message)

def sendToManager(message):
    if("entry" in message):
        um = librarian.User_manager(message["entry"][0]["messaging"][0]["sender"]["id"])
        try:
            um.user_event("MESSAGE",str(message["entry"][0]["messaging"][0]["message"]["text"]))
        except Exception as e:
            print(e)
            um.user_event("MESSAGE",str(message["entry"][0]["messaging"][0]["message"]["attachments"][0]["url"]))
        return True
    else:
        um = librarian.User_manager(int(message["state"]))
        um.user_event("MESSAGE",str(message["code"]))
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
        try:
            print("\nReceived ="+str(json.loads(msg.body)))
            status = work(json.loads(msg.body))
            msg.delete()
        except Exception as e:
            print(e)
    time.sleep(0.2)


