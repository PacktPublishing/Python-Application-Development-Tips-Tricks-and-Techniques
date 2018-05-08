import os

from pytest_bdd import scenario, given, when, then
from src.flickr_downloader import FlickrDownloader


@scenario('get_photo_list.feature', 'Flickr returns a correct list of photos')
def test_get_photo_list():
    pass


@given("a valid Flickr API key")
def valid_api_key(tmpdir):
    return {"downloader": FlickrDownloader("{}".format(os.environ["FLICKR_API_KEY"]), str(tmpdir))}


@when("we request a list of photos from Flickr")
def request_photos(valid_api_key):
    valid_api_key["response"] = valid_api_key["downloader"].get_photo_list()


@then("we should receive a response of dict type")
def receive_response(valid_api_key):
    res = valid_api_key["response"]
    assert type(res) is dict


@then('there should be a "photos" field in the response')
def photos_in_response(valid_api_key):
    res = valid_api_key["response"]
    assert "photos" in res


@then('there should be a "photo" field in response["photos"]')
def photo_in_response_photos(valid_api_key):
    res = valid_api_key["response"]
    assert "photo" in res["photos"]


@then('there should be a list of dicts in response["photos"]["photo"]')
def list_in_response_photos_photo(valid_api_key):
    res = valid_api_key["response"]
    photo_list = res["photos"]["photo"]
    assert type(photo_list) is list
    for photo in photo_list:
        assert type(photo) is dict


@then('each dict in the list should contain the fields "id", "farm", "server" and "secret"')
def photo_files_in_response(valid_api_key):
    res = valid_api_key["response"]
    photo_list = res["photos"]["photo"]

    for photo in photo_list:
        assert "id" in photo
        assert "farm" in photo
        assert "server" in photo
        assert "secret" in photo
