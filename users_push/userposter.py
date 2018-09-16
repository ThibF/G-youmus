import subprocess
from config import config
from string import Template
import logging


def send_message(txt, user_id):
    curl_command = Template(
        "curl -X POST -H \"Content-Type: application/json\" -d '{  \"recipient\": { \"id\": \"$userId\" },\"message\": { \"text\": \"$msg\"  }}' \"https://graph.facebook.com/v2.6/me/messages?access_token=$token\" ")
    request = curl_command.substitute(userId=user_id, msg=txt, token=config["tokenFacebook"])
    logging.debug(request)
    subprocess.check_call(request, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
