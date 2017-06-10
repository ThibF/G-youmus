from flask import Flask
from flask import request
import subprocess
import sys

with open('log','a') as logFile:
    logFile.write("App launched\n")

app = Flask(__name__)

@app.route('/new/ako/zrt/')
def hello_world():
    with open('log','a') as logFile:
        logFile.write(str(request))
    try:
        url = request.args.get('url').strip()
    except Exception as e:
        return "URL not correct"
    try:
        title = request.args.get('title').strip()
    except Exception as e:
        return "Title not correct"
    uid=url[-11:]
    command=["youtube-dl"]
    command.append("--add-metadata")
    command.append("--extract-audio")
    command.append("--audio-format")
    command.append("mp3")
    command.append("-o")
    command.append("music/%(title)s.%(ext)s")
    command.append(uid)

    with open('log','a') as logFile:
        logFile.write(str(command))
        logFile.write("uid/"+str(uid)+"/")
    subprocess.check_call(command)
    return "SUCCESS,"+str(title)+".mp3 in process"
