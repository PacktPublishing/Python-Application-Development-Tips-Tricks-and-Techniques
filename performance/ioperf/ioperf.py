import requests
import os
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_photo_list():
    url = "https://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key=%s&format=json&nojsoncallback=1" % os.environ["FLICKR_API_KEY"]

    res = requests.get(url).json()

    return res


def download_photo(_photo):
    photo_url = "https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (_photo["farm"], _photo["server"], _photo["id"], _photo["secret"])

    photo_res = requests.get(photo_url)

    return photo_res.content


def save_photo(_photo, _photo_content):
    with open(os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", "downloaded", _photo["id"] + ".jpg"), "wb") as photo_file:
        photo_file.write(_photo_content)


if __name__ == "__main__":
    photos_list_res = get_photo_list()

    photo_list = photos_list_res["photos"]["photo"]

    for photo in photo_list:
        photo_content = download_photo(photo)
        save_photo(photo, photo_content)

