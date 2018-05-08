import os

from flickr_downloader import FlickrDownloader


class TestFlickrDownloaderIntegration(object):
    def test_get_get_photo_list(self, tmpdir):
        downloader = FlickrDownloader("{}".format(os.environ["FLICKR_API_KEY"]), str(tmpdir))

        photo_list = downloader.get_photo_list()

        assert "photos" in photo_list
        assert "photo" in photo_list["photos"]

        for photo in photo_list["photos"]["photo"]:
            assert "id" in photo
            assert "farm" in photo
            assert "server" in photo
            assert "id" in photo
            assert "secret" in photo

    def test_download_interesting_photos(self, tmpdir):
        downloader = FlickrDownloader("{}".format(os.environ["FLICKR_API_KEY"]), str(tmpdir))

        downloader.download_interesting_photos()

        assert len(os.listdir(tmpdir)) == 100
        
        for file in os.listdir(tmpdir):
            filename = os.fsdecode(file)
            assert filename.endswith(".jpg")
