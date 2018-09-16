from unittest import TestCase, mock

from media.downloader import Downloader


class TestDownloader(TestCase):
    def test_is_a_correct_url(self):
        downloader = Downloader()
        ret = downloader.is_a_correct_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertTrue(ret)

    @mock.patch('subprocess.check_output')
    def test_is_a_correct_url_facebook(self, subproc_mock):
        downloader = Downloader()
        subproc_mock.return_value = """<html><head><meta charset="utf-8" /></head><body><script type="text/javascript">document.location.replace("https:\/\/www.youtube.com\/watch?v=5-sfG8BV8wU");</script><script type="text/javascript">setTimeout("(new Image()).src=\"\\\/laudit.php?r=JS&u=https\\u00253A\\u00252F\\u00252Fwww.youtube.com\\u00252Fwatch\\u00253Fv\\u00253D5-sfG8BV8wU\";",5000);</script></body></html""".encode()
        ret = downloader.is_a_correct_url("l.facebook.com")
        self.assertTrue(ret)
        subproc_mock.assert_called_with(["curl", "l.facebook.com"])

    def test_is_a_correct_url_failed(self):
        downloader = Downloader()
        ret = downloader.is_a_correct_url("youtube")
        self.assertFalse(ret)

    def test_is_a_correct_url_short(self):
        downloader = Downloader()
        ret = downloader.is_a_correct_url("dQw4w9WgXcQ")
        self.assertTrue(ret)

    def test_is_a_correct_url_too_long(self):
        downloader = Downloader()
        ret = downloader.is_a_correct_url("https://www.youtube.com/watch?v=wZZ7oFKsKzY")
        self.assertFalse(ret)


""" def test_process_url(self):
        self.fail() """
