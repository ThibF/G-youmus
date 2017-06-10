from gmusicapi import Musicmanager
import subprocess
import sys
import glob
import os
from time import sleep
import httplib2

class Uploader():
    def __init__(self):
         self.mm = Musicmanager()
         self.o=self.mm.perform_oauth()
    def check(self):
        while True:
             if self.o._expires_in()<100:
                 print("refresh")
                 http = httplib2.Http()
                 self.o.refresh(http)
             files=glob.glob("./music/*.mp3")
             print("Found :"+str(files))
             for music in files:
                  try:
                      code=self.uploadFile(music)
                      print(code)
                      if len(code[0])==1:
                          try:
                              os.remove(music)
                          except OSError:
                              pass
                  except TypeError as e:
                      try:
                          self.mm.login()
                      except gmusicapi.exceptions.AlreadyLoggedIn as e:
                          pass
             sleep(60)

    def uploadFile(self,path):
        try:
            return self.mm.upload(path)
        except Exception as e:
            print(e)

def main():
    u=Uploader()
    u.check()

if __name__ == "__main__":
    main()
