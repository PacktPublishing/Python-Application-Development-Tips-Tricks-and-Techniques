import os

import pytest
import requests
from requests import RequestException

from flickr_downloader import FlickrDownloader, FlickrDownloaderException


class TestFlickrDownloader(object):
    def test_init_correct(self, tmpdir):
        try:
            FlickrDownloader("testkey", str(tmpdir))
        except FlickrDownloaderException as e:
            pytest.fail(e)

    def test_init_missing_download_folder(self):
        with pytest.raises(FlickrDownloaderException):
            FlickrDownloader("testkey", "amissingfolder")

    def test_init_download_folder_not_a_folder(self, tmpdir):
        f = tmpdir.join("afile.txt")
        f.write("test text")

        with pytest.raises(FlickrDownloaderException):
            FlickrDownloader("testkey", str(f))

    def test_init_api_key_none(self, tmpdir):
        with pytest.raises(FlickrDownloaderException):
            FlickrDownloader(None, str(tmpdir))

    def test_init_api_key_empty(self, tmpdir):
        with pytest.raises(FlickrDownloaderException):
            FlickrDownloader("", str(tmpdir))

    def test_get_photo_list_correct_url(self, tmpdir, mocker):
        response_mock = mocker.MagicMock()
        response_mock.json = mocker.MagicMock(return_value="valid json here")

        mocker.patch.object(requests, "get", return_value=response_mock)

        downloader = FlickrDownloader("test_key", str(tmpdir))

        photo_list = downloader.get_photo_list()

        assert photo_list == "valid json here"

        url = "https://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key=%s&format=json&nojsoncallback=1" % "test_key"

        requests.get.assert_called_once_with(url)

    def test_get_photo_list_failed_request(self, tmpdir, mocker):
        mocker.patch.object(requests, "get", side_effect=RequestException("test exception"))

        downloader = FlickrDownloader("test_key", str(tmpdir))

        with pytest.raises(FlickrDownloaderException):
            downloader.get_photo_list()

    def test_download_photo_correct(self, tmpdir, mocker):
        response_mock = mocker.MagicMock()
        response_mock.content = "test photo content"

        mocker.patch.object(requests, "get", return_value=response_mock)

        downloader = FlickrDownloader("test_key", str(tmpdir))

        photo = {
            "farm": "testfarm",
            "server": "testserver",
            "id": "testid",
            "secret": "testsecret"
        }

        photo_content = downloader.download_photo(photo.copy())

        assert photo_content == "test photo content"
        photo_url = "https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (photo["farm"], photo["server"], photo["id"], photo["secret"])
        requests.get.assert_called_once_with(photo_url)

    def test_download_photo_missing_keys(self, tmpdir, mocker):
        response_mock = mocker.MagicMock()
        response_mock.content = "test photo content"

        mocker.patch.object(requests, "get", return_value=response_mock)

        downloader = FlickrDownloader("test_key", str(tmpdir))

        photo = {
            "server": "testserver",
            "id": "testid",
            "secret": "testsecret"
        }

        with pytest.raises(FlickrDownloaderException):
            downloader.download_photo(photo)

        photo = {
            "farm": "testfarm",
            "id": "testid",
            "secret": "testsecret"
        }

        with pytest.raises(FlickrDownloaderException):
            downloader.download_photo(photo)

        photo = {
            "farm": "testfarm",
            "server": "testserver",
            "secret": "testsecret"
        }

        with pytest.raises(FlickrDownloaderException):
            downloader.download_photo(photo)

        photo = {
            "farm": "testfarm",
            "server": "testserver",
            "id": "testid"
        }

        with pytest.raises(FlickrDownloaderException):
            downloader.download_photo(photo)

    def test_download_photo_failed_request(self, tmpdir, mocker):
        mocker.patch.object(requests, "get", side_effect=RequestException("test exception"))
        downloader = FlickrDownloader("test_key", str(tmpdir))

        photo = {
            "farm": "testfarm",
            "server": "testserver",
            "id": "testid",
            "secret": "testsecret"
        }

        with pytest.raises(FlickrDownloaderException):
            downloader.download_photo(photo)

    def test_download_interesting_photos_correct(self, tmpdir, mocker):
        photos_list_mock = {
            "photos": {
                "photo": [
                    {
                        "id": "1"
                    },
                    {
                        "id": "2"
                    },
                    {
                        "id": "3"
                    }
                ]
            }
        }

        # Mock the downloader class
        get_photo_list_mock = mocker.patch.object(FlickrDownloader, "get_photo_list")
        download_photo_mock = mocker.patch.object(FlickrDownloader, "download_photo")
        save_photo_mock = mocker.patch.object(FlickrDownloader, "_FlickrDownloader__save_photo")

        get_photo_list_mock.return_value = photos_list_mock
        download_photo_mock.return_value = "photo content"

        downloader = FlickrDownloader("test_key", str(tmpdir))

        downloader.download_interesting_photos()

        get_photo_list_mock.assert_called_once()
        download_photo_mock.assert_any_call({"id": "1"})
        download_photo_mock.assert_any_call({"id": "2"})
        download_photo_mock.assert_any_call({"id": "3"})
        save_photo_mock.assert_any_call(os.path.join(str(tmpdir), "1.jpg"), "photo content")
        save_photo_mock.assert_any_call(os.path.join(str(tmpdir), "2.jpg"), "photo content")
        save_photo_mock.assert_any_call(os.path.join(str(tmpdir), "3.jpg"), "photo content")
