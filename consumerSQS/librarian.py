from oauth2client.client import OAuth2WebServerFlow, TokenRevokeError
import oauth2client.file
from config import config
import os
from gmusicapi import Musicmanager
import subprocess
import sys
import glob
import os
from time import sleep
import httplib2
from collections import namedtuple
import answer
import urllib
import pickle

OAuthInfo = namedtuple('OAuthInfo', 'client_id client_secret scope redirect')
oauth = OAuthInfo(
    '652850857958.apps.googleusercontent.com',
    'ji1rklciNp2bfsFJnEH_i6al',
    'https://www.googleapis.com/auth/musicmanager',
    'urn:ietf:wg:oauth:2.0:oob'
)

class User_state():
    def __init__(self,userId):
        self.userId = userId
        self.state = None
        self.queue = []
        self.metadataState = None

class User_manager():

    userId = None
    user_state = None
    def __init__(self,userId):
        self.userId = userId
        self.folder_path = config["library_path"]+str(userId)+"/"
        try:
            os.mkdir(self.folder_path)
            self.user_state = User_state()
        except Exception as e:
            self.user_state = reconstruct_user_state(self.userId)

    def build_user_file(user_state):
        pickle.dump(user_state, open(self.folder_path+"state.p","wb"))
        return True
    def reconstruct_user_state(userId):
        user_state = pickle.load(open(self.folder_path+"state.p", 'rb'))
        return user_state

    def user_event(event,payload):
        if self.user_state.state = None:
            ask_credentials()
            self.user_state.state = "CREDENTIALS WAITING"
        if self.user_state.state = "CREDENTIALS WAITING"
            verify_credentials(payload)



    def ask_credentials():
        flow = OAuth2WebServerFlow(*oauth)
        auth_uri = flow.step1_get_authorize_url()
        answer.send_message("Please follow the link and paste the code back to me !",self.userId)
        answer.send_message(auth_uri,self.userId)
        return
    def verify_credentials(code):
        credentials = flow.step2_exchange(code)
        storage = oauth2client.file.Storage(self.folder_path+"oauth.cred")
        storage.put(credentials)
        mm=Musicmanager()
        mm.perform_oauth(storage_filepath = folder_path+"oauth.cred")
