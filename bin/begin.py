#!/usr/bin/python
from gmusicapi import Musicmanager
import sys, getopt

def main(argv):
    mm = Musicmanager()
    isIncremental= False
    isDryRun= False
    try:
        opts, args = getopt.getopt(argv,"ID",[])
    except getopt.GetoptError:
        print("[I]")
        sys.exit(2)
    for opt,arg in opts:
        if opt =="-I":
            isIncremental= True
        elif opt=="-D":
            isDryRun= True
    try:
        mm.login()
    except Exception as e:
        print(e)
        mm.perform_oauth()
    listMusicsUploaded=mm.get_uploaded_songs()
    print(listMusicsUploaded)
    if not isIncremental:
        print("HEY")
    else:
        print("not currently supported")

if __name__ == "__main__":
    main(sys.argv[1:])
