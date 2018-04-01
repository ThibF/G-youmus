import json
import re

class MessageFacebook:
    def __init__(self,body):
        self.body = json.loads(body)
        if type(self.body) == str :
            self.body = json.loads(self.body)
        if type(self.body)==str :
            self.body = json.loads(self.body)
    def get_sender_id(self):
        sender_id = self.body["entry"][0]["messaging"][0]["sender"]["id"]
        return sender_id
    
    def get_text(self):    
        text = self.body["entry"][0]["messaging"][0]["message"]["text"]
        return text
    def get_url(self):
        url = ""
        try : 
            url = self.body["entry"][0]["messaging"][0]["message"]["attachments"][0]["url"]
        except Exception as e:
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', self.get_text())
            if len(urls) > 0:
                url = urls[0]
        if len(url)<1:
            raise AttributeError
        return url
    def get_code(self):
        return self.body["code"]
    def get_state(self):
        return self.body["state"]