import subprocess
from config import config
from string import Template
import logging

def send_message(txt,userId):
    curlCommand = Template ("curl -X POST -H \"Content-Type: application/json\" -d '{  \"recipient\": { \"id\": \"$userId\" },\"message\": { \"text\": \"$msg\"  }}' \"https://graph.facebook.com/v2.6/me/messages?access_token=$token\" ")
    request=curlCommand.substitute(userId=userId,msg=txt,token=config["tokenFacebook"])
    logging.debug(request)
    print(request)
    subprocess.check_call(request,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

