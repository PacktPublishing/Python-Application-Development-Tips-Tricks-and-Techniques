import os

from pytest_bdd import scenario, given, when, then
from src.flickr_downloader import FlickrDownloader


@scenario('download_interesting_photos.feature', 'Flickr sends out 100 interesting photos')
def test_download_interesting_photos():
    pass


@given('a valid Flickr API key and a valid download directory')
def valid_api_key(tmpdir):
    return {"downloader": FlickrDownloader("{}".format(os.environ["FLICKR_API_KEY"]), str(tmpdir)),
            "tmpdir": tmpdir}


@when('we request to download 100 interesting photos from Flickr')
def download_photos(valid_api_key):
    downloader = valid_api_key["downloader"]
    downloader.download_interesting_photos()


@then('the download directory should contain 100 files')
def receive_response(valid_api_key):
    tmpdir = valid_api_key["tmpdir"]
    assert len(os.listdir(tmpdir)) == 100


@then('all the file names in the download directory should end with ".jpg"')
def photos_in_response(valid_api_key):
    tmpdir = valid_api_key["tmpdir"]
    for file in os.listdir(tmpdir):
        filename = os.fsdecode(file)
        assert filename.endswith(".jpg")
