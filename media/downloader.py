import glob
import re
import subprocess
from config import config
import youtube_dl as youtube_dl

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
                return True
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

    def process_metadata(self, fullInformation):
        if "_type" in fullInformation and fullInformation["_type"] == "playlist":
            for entrie in fullInformation["entries"]:
                artist = self.choose_artist(entrie)
                if artist is not None:
                    self.add_metadata(config["library_path"] + "/" + str(entrie["title"]) + ".mp3", artist)
        else:
            artist = self.choose_artist(fullInformation)
            if artist is not None:
                self.add_metadata(config["library_path"] + "/" + str(fullInformation["title"]) + ".mp3", artist)

    def is_title_with_artist(self, title):
        return False

    def process_url(self, url, path):
        if "l.facebook.com" in url:
            fb_redirection = subprocess.check_output(["curl", url])
            p = re.compile('watch\?v=(.{11})\"')
            uid = p.search(fb_redirection.decode('ascii')).group(1)
        else:
            uid = url
        ydl_opts_download['outtmpl'] = config["library_path"] + "/" + '%(title)s.%(ext)s'
        fullInformation = youtube_dl.YoutubeDL(ydl_opts_title).extract_info(uid)
        youtube_dl.YoutubeDL(ydl_opts_download).download([uid])
        files = glob.glob(config["library_path"] + "/*.mp3")
        self.process_metadata(fullInformation)
        return files
