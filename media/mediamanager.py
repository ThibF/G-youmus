import logging

from media.downloader import Downloader
from media.uploader import Uploader
from users_push.userslibrarian import UsersLibrarian


class MediaManager:
    downloader = None

    def __init__(self):
        self.downloader = Downloader()
        self.uploader = Uploader()

    def is_correct_url(self, url):
        return self.downloader.is_a_correct_url(url)

    def transfer_url(self, url, user_state):
        logging.info("Download of "+str(url)+"will begin")
        downloads = self.downloader.process_url(url, UsersLibrarian.path_user(user_state.user_id))
        logging.info("All files ("+str(len(downloads))+") downloaded:"+str(downloads))

        self.uploader.upload(downloads, user_state)
        logging.info("All files ("+str(len(downloads))+") are uploaded:"+str(downloads))
        self.downloader.clean(downloads)


