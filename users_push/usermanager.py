import logging
from collections import namedtuple

import oauth2client.file
from gmusicapi import Musicmanager
from oauth2client.client import OAuth2WebServerFlow

from media.mediamanager import MediaManager
from users_push.userhostess import UserHostess
from users_push.userslibrarian import *
from users_push.userstate import UserState

OAuthInfo = namedtuple('OAuthInfo', 'client_id client_secret scope redirect')
oauth = OAuthInfo(
    '794418103801-69gbuc7jmlnitpflnmbjqdq3bgimecji.apps.googleusercontent.com',
    '-_6HrNIO-zDO6a0fSm_drOkR',
    'https://www.googleapis.com/auth/musicmanager',
    'https://phagekwmf7.execute-api.us-west-2.amazonaws.com/Prod/identification'
)


class UserManager:
    user_hostess = None
    media_manager = None
    users_librarian = None

    def __init__(self):
        self.user_hostess = UserHostess()
        self.media_manager = MediaManager()
        self.users_librarian = UsersLibrarian()

    def init_users(self):
        self.users_librarian.init_users()

    def is_new_user(self, user_id):
        try:
            self.users_librarian.load_user(user_id)
            return False
        except FileNotFoundError:
            return True

    def create_user(self, user_id):
        user_state = UserState(user_id)
        self.user_hostess.greet_user(user_id)
        self.users_librarian.write_user(user_state)
        return user_state

    def is_user_logged(self, user_id):
        mm = Musicmanager()
        mm.login(oauth_credentials=self.users_librarian.path_user_cred(user_id),
                 uploader_id='3C:F8:62:67:01:0B')
        # TODO which error to except

    def verify_credentials(self, user_id, code):
        user_state = self.users_librarian.load_user(user_id)
        credentials = user_state.flow.step2_exchange(code)
        storage = oauth2client.file.Storage(UsersLibrarian.path_user_cred(user_id))
        storage.put(credentials)
        mm = Musicmanager()
        mm.login(oauth_credentials=UsersLibrarian.path_user_cred(user_id), uploader_id='3C:F8:62:67:01:0B')

    def user_event(self, event, wrapped_msg):
        user_id = wrapped_msg.get_sender_id()
        payload = wrapped_msg.get_text()
        user_state = self.users_librarian.load_user(user_id)
        logging.debug(user_id + "| " + str(event) + "|" + str(payload))
        if "reset" in payload:
            user_state.state = None
            self.users_librarian.write_user(user_state)
            return
        if user_state.state is None and "MESSAGE" in event:
            self.user_begin_identification(user_state, payload)
        elif "CREDENTIALS WAITING" in user_state.state and "IDENTIFICATION" in event:
            self.user_end_identification(user_state, wrapped_msg.get_code())
        elif "CREDENTIALS WAITING" in user_state.state:
            self.user_begin_identification(user_state, payload)
        elif "SET UP COMPLETED" in user_state.state:
            if not self.media_manager.is_correct_url(payload):
                logging.warn("Url not understood:"+str(payload))
                self.user_hostess.request_not_understood(user_id)
            else:
                logging.info("Url understood")
                self.media_manager.transfer_url(payload, user_state)
                user_state.count += 1
                self.user_hostess.upload_succeeded(user_id)

    def user_begin_identification(self, user_state, payload):
        self.ask_credentials(user_state.user_id)
        user_state = self.users_librarian.load_user(user_state.user_id)
        user_state.state = "CREDENTIALS WAITING"
        self.users_librarian.write_user(user_state)

    def user_end_identification(self, user_state, payload):
        self.verify_credentials(user_state.user_id, payload)
        self.user_hostess.identification_completed_user(user_state.user_id)
        user_state.state = "SET UP COMPLETED"
        self.users_librarian.write_user(user_state)

    def ask_credentials(self, user_id):
        user_state = self.users_librarian.load_user(user_id)
        user_state.flow = OAuth2WebServerFlow(*oauth)
        auth_uri = user_state.flow.step1_get_authorize_url() + "&state=" + str(user_id + "&prompt=consent")
        self.users_librarian.write_user(user_state)
        self.user_hostess.identification_user(user_id)
        self.user_hostess.user_identification_url(user_id, auth_uri)
