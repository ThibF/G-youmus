import json


class FacebookMessage:
    def __init__(self, body):
        self.body = json.loads(body)
        if type(self.body) == str:
            self.body = json.loads(self.body)
        if type(self.body) == str:
            self.body = json.loads(self.body)

    def get_sender_id(self):
        sender_id = self.body["entry"][0]["messaging"][0]["sender"]["id"]
        return sender_id

    def get_text(self):
        text = self.body["entry"][0]["messaging"][0]["message"]["text"]
        return text

    def get_url(self):
        url = ""
        if len(url) < 1:
            raise AttributeError
        return url
