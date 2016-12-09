import pytest
from librarian import Librarian
import mock
from gmusicapi import Musicmanager

def test_librarian_add():
    mm=mock.Mock()
    
    libr=Librarian("user",mm)
    libr.add_music("music")
    assert len(libr.fifo_upload)>0
