import logging
import time

from fifo_parser.facebookmessage import FacebookMessage
from fifo_parser.messageslistener import MessagesListener
from users_push.usermanager import UserManager


class MessageExecutor:

    def __init__(self):
        self.msg_listener = MessagesListener()
        self.user_manager = UserManager()
        self.user_manager.init_users()

    def run(self):
        while True:
            wrapped_message = self.msg_listener.receive_messages()
            if wrapped_message is None:
                pass
            else:
                self.execute_message(wrapped_message)
            time.sleep(0.2)

    def execute_message(self, message):
        logging.info("Execute:"+str(message.body))
        if self.user_manager.is_new_user(message.get_sender_id()):
            self.user_manager.create_user(message.get_sender_id())

        if type(message) == FacebookMessage:
            self.user_manager.user_event("MESSAGE", message)
        else:
            self.user_manager.user_event("IDENTIFICATION", message)
        return True
