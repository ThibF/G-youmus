from gmusicapi import *
import logging
from users_push.userslibrarian import *


class Uploader:

    def upload(self, files, user_state):
        cred_path = UsersLibrarian.path_user_cred(user_state.user_id)
        for music in files:
            mm = Musicmanager(debug_logging=False)
            mm.logger.setLevel(logging.WARNING)
            mm.login(oauth_credentials=cred_path, uploader_id='02:42:3D:5B:ED:7B')
            code = mm.upload(music)
            logging.info(str(music)+" was uploaded with return value:"+str(code))
            try:
                os.remove(music)
            except OSError:
                pass
