import pytest
import os
from specific_flickr_downloader.specific_flickr_downloader import download_specific_photo
from specific_flickr_downloader.specific_flickr_downloader import FlickrDownloader


class TestSpecificFlickrDownloader(object):
    def test_download_specific_photo(self, tmpdir, mocker):
        photo_id = "2"
        download_location = str(tmpdir)
        expected_return = os.path.join(tmpdir, "{}.jpg".format(photo_id))
        flickr_api_key = "testkey"

        flickr_downloader_init_mock = mocker.patch.object(FlickrDownloader, "__init__")
        get_photo_list_mock = mocker.patch.object(FlickrDownloader, "get_photo_list")
        download_photo_mock = mocker.patch.object(FlickrDownloader, "download_photo")
        save_photo_mock = mocker.patch.object(FlickrDownloader, "save_photo")

        flickr_downloader_init_mock.return_value = None

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

        get_photo_list_mock.return_value = photos_list_mock
        download_photo_mock.return_value = "photo content"

        returned_value = download_specific_photo(photo_id, download_location, flickr_api_key)

        assert expected_return == returned_value
        save_photo_mock.assert_called_once_with(expected_return, "photo content")
