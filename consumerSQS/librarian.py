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
import re

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
    folder_path = None 
    def __init__(self,userId):
        self.userId = userId
        self.folder_path = config["library_path"]+str(userId)+"/"
        try:
            os.mkdir(self.folder_path)
            self.user_state = User_state(userId)
        except Exception as e:
            try:
                self.user_state = self.reconstruct_user_state(self.userId)
            except Exception as e:
                print("USER NOT FOUND, SHOULD NOT HAPPEN")
                self.user_state = User_state(userId)
    def build_user_file(self,user_state):
        pickle.dump(user_state, open(self.folder_path+"state.p","wb"))
        return True
    def reconstruct_user_state(self,userId):
        user_state = pickle.load(open(self.folder_path+"state.p", 'rb'))
        return user_state

    def user_event(self,event,payload):

        try:
            if self.user_state.state is None:
                self.ask_credentials()
                self.user_state.state = "CREDENTIALS WAITING"
            elif "CREDENTIALS WAITING" in self.user_state.state :
                self.verify_credentials(payload)
                answer.send_message("Hey everything is setup !",self.userId)
                self.user_state.state = "SET UP COMPLETED"
            elif "SET UP COMPLETED" in self.user_state.state :
                self.process_url(payload)
                self.user_state.state = "PROCESSING LINK"

            self.build_user_file(self.user_state)
        except Exception as e:
            print(e)
            answer.send_message("Outch !",self.userId)
            answer.send_message("Something gone wrong",self.userId)
            answer.send_message("I will keep you informed",self.userId)
            self.user_state.state = None
            self.build_user_file(self.user_state)

    def process_url(self, url):
        fb_redirection = subprocess.check_output(["curl",url])
        print(fb_redirection.decode('ascii'))
        p = re.compile('watch\?v=(.{11})\"')
        uid = p.search(fb_redirection.decode('ascii')).group(1)
        print(uid)
        command=["youtube-dl"]
        command.append("--add-metadata")
        command.append("--extract-audio")
        command.append("--audio-format")
        command.append("mp3")
        command.append("-o")
        command.append(self.folder_path+"/%(title)s.%(ext)s")
        command.append(uid)
        subprocess.check_call(command)
        files=glob.glob(self.folder_path+"/*.mp3")
        for music in files:
            try:
                mm=Musicmanager()
                mm.login(oauth_credentials = self.folder_path+"oauth.cred")
                code=mm.upload(music)
                print(code)
                if len(code[0])==1:
                    try:
                        os.remove(music)
                    except OSError:
                        pass
            except TypeError as e:
                print(e)
                try:
                    mm.login()
                except gmusicapi.exceptions.AlreadyLoggedIn as e:
                    pass

    def ask_credentials(self):
        self.user_state.flow = OAuth2WebServerFlow(*oauth)
        auth_uri = self.user_state.flow.step1_get_authorize_url()
        answer.send_message("Please follow the link and paste the code back to me !",self.userId)
        answer.send_message(auth_uri,self.userId)
        return
    def verify_credentials(self,code):
        credentials = self.user_state.flow.step2_exchange(code)
        storage = oauth2client.file.Storage(self.folder_path+"oauth.cred")
        storage.put(credentials)
        mm=Musicmanager()
        mm.login(oauth_credentials = self.folder_path+"oauth.cred")
