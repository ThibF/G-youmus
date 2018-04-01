import boto3
import logging
from config import config
import answer
import json
import time
import librarian

def work(message):
    return sendToManager(message)

def sendToManager(message):
    logging.debug("Manager received:"+str(message))
    
    try:
        um = librarian.User_manager(message.get_sender_id())
        try:
            um.user_event("MESSAGE",message.get_text())
        except Exception as e:
            print(e)
            um.user_event("MESSAGE",message.get_url())
    except KeyError as e:
        um = librarian.User_manager(message.get_state())
        um.user_event("IDENTIFICATION",message.get_code())
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




