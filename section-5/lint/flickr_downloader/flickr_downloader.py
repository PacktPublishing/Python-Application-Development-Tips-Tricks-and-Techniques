"""Download 100 interesting photos from Flickr"""
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def __get_photo_list(api_key):
    url = "https://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key=%s&format=json&nojsoncallback=1" % api_key

    res = requests.get(url).json()

    return res


def __download_photo(_photo):
    photo_url = "https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (_photo["farm"], _photo["server"], _photo["id"], _photo["secret"])

    photo_res = requests.get(photo_url)

    return photo_res.content


def __save_photo(_photo, _photo_content, location):
    with open(os.path.join(location, _photo["id"] + ".jpg"), "wb") as photo_file:
        photo_file.write(_photo_content)


def download_interesting_photos(flickr_api_key, location):
    """Download 100 interesting Flickr photos

    Arguments:
    flickr_api_key -- the API key used to request the photos from Flickr
    location -- download location for the photos (must exist and be writable)
    """
    photos_list_res = __get_photo_list(flickr_api_key)

    photo_list = photos_list_res["photos"]["photo"]

    with ThreadPoolExecutor() as executor:
        future_photos = {executor.submit(__download_photo, photo): photo for photo in photo_list}

        for future in as_completed(future_photos):
            photo_content = future.result()
            __save_photo(future_photos[future], photo_content, location)
