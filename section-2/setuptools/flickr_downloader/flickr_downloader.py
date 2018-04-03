import requests
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def __get_photo_list():
    url = "https://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key=%s&format=json&nojsoncallback=1" % os.environ["FLICKR_API_KEY"]

    res = requests.get(url).json()

    return res


def __download_photo(_photo):
    photo_url = "https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (_photo["farm"], _photo["server"], _photo["id"], _photo["secret"])

    photo_res = requests.get(photo_url)

    return photo_res.content


def __save_photo(_photo, _photo_content, location):
    with open(os.path.join(location, _photo["id"] + ".jpg"), "wb") as photo_file:
        photo_file.write(_photo_content)


def download_interesting_photos(location):
    photos_list_res = __get_photo_list()

    photo_list = photos_list_res["photos"]["photo"]

    with ThreadPoolExecutor() as e:
        future_photos = {e.submit(__download_photo, photo): photo for photo in photo_list}

        for future in as_completed(future_photos):
            photo_content = future.result()
            __save_photo(future_photos[future], photo_content, location)
