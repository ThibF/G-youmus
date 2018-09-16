import time


class UserState:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = None
        self.queue = []
        self.metadataState = None
        self.count = 0
        self.creationTimestamp = time.time()
        self.lastInteractionTimestamp = time.time()
        self.flow = None
