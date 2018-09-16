import json


class GoogleMessage:
    def __init__(self, body):
        self.body = json.loads(body)
        if type(self.body) == str:
            self.body = json.loads(self.body)
        if type(self.body) == str:
            self.body = json.loads(self.body)

    def get_sender_id(self):
        return self.body["state"]

    def get_text(self):
        return self.body

    def get_code(self):
        return self.body["code"]
