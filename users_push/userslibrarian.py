import os
import pickle
from config import config


class UsersLibrarian:

    @staticmethod
    def init_users():
        try:
            os.mkdir(config["library_path"])
        except FileExistsError:
            pass

    @staticmethod
    def load_user(user_id):
        user_state = pickle.load(open(config["library_path"] + "/" + user_id + "/" + "state.p", "rb"))
        return user_state

    @staticmethod
    def write_user(user_state):
        try:
            os.mkdir(config["library_path"] + "/" + user_state.user_id)
        except FileExistsError:
            pass
        pickle.dump(user_state, open(config["library_path"] + "/" + user_state.user_id + "/" + "state.p", "wb"))

    @staticmethod
    def path_user_cred(user_id):
        return config["library_path"] + "/" + user_id + "/oauth.cred"

    @staticmethod
    def path_user(user_id):
        return config["library_path"] + "/" + user_id + "/"
