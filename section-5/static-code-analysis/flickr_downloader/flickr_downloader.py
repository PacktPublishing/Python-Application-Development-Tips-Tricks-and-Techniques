import requests
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import RequestException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FlickrDownloaderException(Exception):
    pass


class FlickrDownloader:
    def __init__(self, api_key, download_location):
        if not isinstance(api_key, str):
            raise FlickrDownloaderException("api_key should be str")

        if not isinstance(download_location, str):
            raise FlickrDownloaderException("download_location should be str")

        if api_key is None or len(api_key) == 0:
            raise FlickrDownloaderException("API Key is not set")

        if not os.path.exists(download_location) or not os.path.isdir(download_location):
            raise FlickrDownloaderException("Download location does not exist or is not a directory")

        self.__api_key = api_key
        self.__download_location = download_location

    def get_photo_list(self):
        url = "https://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key=%s&format=json&nojsoncallback=1" % self.__api_key

        try:
            res = requests.get(url).json()
        except RequestException as e:
            raise FlickrDownloaderException("Request error: %s", e)

        return res

    @staticmethod
    def download_photo(photo):
        try:
            photo_url = "https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (photo["farm"], photo["server"], photo["id"], photo["secret"])
        except KeyError as e:
            raise FlickrDownloaderException("photo argument is invalid: %s" % e)

        try:
            photo_res = requests.get(photo_url)
        except RequestException as e:
            raise FlickrDownloaderException("Request error: %s", e)

        return photo_res.content

    def download_interesting_photos(self):
        photos_list_res = self.get_photo_list()

        photo_list = photos_list_res["photos"]["photo"]

        with ThreadPoolExecutor() as e:
            future_photos = {e.submit(self.download_photo, photo): photo for photo in photo_list}

            for future in as_completed(future_photos):
                photo_content = future.result()
                photo = future_photos[future]
                self.__save_photo(os.path.join(self.__download_location, photo["id"] + ".jpg"), photo_content)

    @staticmethod
    def __save_photo(filename, photo_content):
        try:
            with open(filename, "wb") as photo_file:
                photo_file.write(photo_content)
        except IOError as e:
            raise FlickrDownloaderException("Failed to save photo: %s", e)
