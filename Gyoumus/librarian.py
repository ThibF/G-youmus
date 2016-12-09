class Librarian():
    """ Will know and manage your Music library 
    """
    def __init__(self,user,music_manager):
        self.user=user
        self.music_manager=music_manager
        self.musics=music_manager.get_uploaded_songs()
        self.fifo_upload=[]
    def isAlreadyUploaded(self,music_to_compare):
        for music in self.musics:
            if(music.title==music_to_compare.title):
                return True
        return False

    def add_music(self,music):
        self.fifo_upload.append(music)
        pass
    def __upload__(self):
        for music in self.fifo_upload:
            self.music_manager.upload(music.path)
        pass

    def uploadSynchronously(self):
        pass

