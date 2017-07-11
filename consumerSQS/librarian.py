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
import time


OAuthInfo = namedtuple('OAuthInfo', 'client_id client_secret scope redirect')
oauth = OAuthInfo(
    '794418103801-69gbuc7jmlnitpflnmbjqdq3bgimecji.apps.googleusercontent.com',
    '-_6HrNIO-zDO6a0fSm_drOkR',
    'https://www.googleapis.com/auth/musicmanager',
    'https://phagekwmf7.execute-api.us-west-2.amazonaws.com/Prod/identification'
)

class User_state():
    def __init__(self,userId):
        self.userId = userId
        self.state = None
        self.queue = []
        self.metadataState = None
        self.count = 0
        self.creationTimestamp = time.time()
        self.lastInteractionTimestamp = time.time() 
class User_manager():

    isTinyURL = False
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
                print("Recover to be done")
                self.user_state = User_state(userId)
    def build_user_file(self,user_state):
        user_state.lastInteractionTimestamp = time.time() 
        pickle.dump(user_state, open(self.folder_path+"state.p","wb"))
        return True
    def reconstruct_user_state(self,userId):
        user_state = pickle.load(open(self.folder_path+"state.p", 'rb'))
        if not hasattr(user_state, 'count'):
            user_state.count = 0 

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
                self.user_state.count += 1
                answer.send_message("Hey niceJob !!",self.userId)
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
        auth_uri = self.user_state.flow.step1_get_authorize_url()+"&state="+str(self.userId+"&prompt=consent")
        answer.send_message("Please follow the link and paste the code back to me !",self.userId)
        try:
            if self.isTinyURL:
                self.ask_tiny_url(auth_uri)
        except Exception as e:
                self.isTinyURL = False
        if not self.isTinyURL:
            self.ask_auth_uri(auth_uri)

        return
    def verify_credentials(self,code):
        credentials = self.user_state.flow.step2_exchange(code)
        storage = oauth2client.file.Storage(self.folder_path+"oauth.cred")
        storage.put(credentials)
        mm=Musicmanager()
        mm.login(oauth_credentials = self.folder_path+"oauth.cred")
    
    def ask_auth_uri(self, auth_uri):
        answer.send_message(auth_uri,self.userId)

    def ask_tiny_url(self,tiny_url):
        tiny_url = subprocess.check_output(["curl","http://tinyurl.com/api-create.php?url="+str(auth_uri)+ "'"])
        answer.send_message(tiny_url.decode("utf-8"),self.userId)
        answer.send_message("Psst, its a tiny URL, dont freakout, its Google behind",self.userId)
