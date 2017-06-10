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

OAuthInfo = namedtuple('OAuthInfo', 'client_id client_secret scope redirect')
oauth = OAuthInfo(
    '652850857958.apps.googleusercontent.com',
    'ji1rklciNp2bfsFJnEH_i6al',
    'https://www.googleapis.com/auth/musicmanager',
    'urn:ietf:wg:oauth:2.0:oob'
)




def user_event(userId,event,payload):
    folder_path = config["library_path"]+str(userId)
    try:
        os.mkdir(folder_path)
    except Exception as e:
        pass
    ask_credentials(userId)




def ask_credentials(userId):
    mm=Musicmanager()
    flow = OAuth2WebServerFlow(*oauth)
    auth_uri = flow.step1_get_authorize_url()
    answer.send_message("Please follow the link and paste the code back to me !",userId)
    answer.send_message(auth_uri,userId)
    return
    print("Visit the following url:\n %s" % auth_uri)
    code = input("Follow the prompts, then paste the auth code here and hit enter: ")
    credentials = flow.step2_exchange(code)
    if storage_filepath is not None:
        if storage_filepath == OAUTH_FILEPATH:
            utils.make_sure_path_exists(os.path.dirname(OAUTH_FILEPATH), 0o700)
        storage = oauth2client.file.Storage(storage_filepath)
    storage.put(credentials)
    mm.perform_oauth(storage_filepath = folder_path+"oauth.cred")
