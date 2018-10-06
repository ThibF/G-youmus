import glob
import os
import re
import shutil
import subprocess
from config import config
import youtube_dl as youtube_dl
import uuid
import fnmatch
from pathlib import Path

ydl_opts_download = {
    'format': 'bestaudio/best',
    'postprocessors': [{'key': 'FFmpegMetadata'},
                       {
                           'key': 'FFmpegExtractAudio',
                           'preferredcodec': 'mp3',
                       }],
    'addmetadata': True,
    'quiet': True,
    'verbose': False,
}
ydl_opts_title = {
    'quiet': True,
    'simulate': True,
}


class Downloader:

    def is_a_correct_url(self, url):
        if "l.facebook.com" in url:
            fb_redirection = subprocess.check_output(["curl", url])
            p = re.compile('watch\?v=(.{11})\"')
            uid = p.search(fb_redirection.decode('ascii')).group(1)
        else:
            uid = url
        try:
            info = youtube_dl.YoutubeDL(ydl_opts_title).extract_info(uid)
            if "_type" in info and info["_type"] == "playlist":
                for music in info['entries']:
                    if music["duration"] > 600:
                        return False
                    # TODO Support playlist correctly : see metadata hell
                return False
            elif info["duration"] < 600:
                return True
            return False
        # Triggered by "Hey niceJob !!https://www.youtube.com/playlist?list=PL3aW5sLM3-BtUIYjBhCgHCVSagK6R3LWi"
        except ValueError:
            return False
        except youtube_dl.DownloadError:
            return False
        except KeyError:
            return False

    def add_metadata(self, path, artist):
        subprocess.check_call(
            ["ffmpeg", "-v", "warning", "-y", "-i", str(path), "-c", "copy", "-metadata", "artist=" + str(artist),
             str(path) + "bis.mp3"])
        subprocess.check_call(["mv", str(path) + "bis.mp3", str(path)])

    def choose_artist(self, information):
        """
        if artist exist
        if cover by take following
        if search

        :param information:
        :return:
        """

        if "artist" in information and information["artist"] is not None:
            return information["artist"]
        elif self.is_title_with_artist(information["title"]):
            return None
        else:
            return information["uploader"]

    def process_metadata(self, fullInformation, folderpath):
        if "_type" in fullInformation and fullInformation["_type"] == "playlist":
            for entrie in fullInformation["entries"]:
                artist = self.choose_artist(entrie)
                if artist is not None:
                    self.add_metadata(config["library_path"] + "/" + str(entrie["title"]) + ".mp3", artist)
        else:
            artist = self.choose_artist(fullInformation)
            filename = fnmatch.filter(os.listdir(folderpath), "*.mp3")[0]
            filepath = folderpath + "/" + filename
            if artist is not None:
                self.add_metadata(filepath, artist)

    def is_title_with_artist(self, title):
        return False

    def process_url(self, url, path):
        if "l.facebook.com" in url:
            fb_redirection = subprocess.check_output(["curl", url])
            p = re.compile('watch\?v=(.{11})\"')
            uid = p.search(fb_redirection.decode('ascii')).group(1)
        else:
            uid = url
        foldername = str(uuid.uuid4())
        folderpath = config["library_path"] + "/" + foldername
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
        ydl_opts_download['outtmpl'] = folderpath + "/" + '%(title)s.%(ext)s'
        fullInformation = youtube_dl.YoutubeDL(ydl_opts_title).extract_info(uid)
        youtube_dl.YoutubeDL(ydl_opts_download).download([uid])
        files = fnmatch.filter(os.listdir(folderpath), "*.mp3")
        files = [folderpath + "/" + file for file in files]
        self.process_metadata(fullInformation, folderpath)
        return files

    def clean(self, files):
        folderToRemove = Path(files[0]).parent
        shutil.rmtree(str(folderToRemove))
