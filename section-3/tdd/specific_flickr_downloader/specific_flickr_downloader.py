import os
from flickr_downloader.flickr_downloader import FlickrDownloader


def download_specific_photo(photo_id, download_folder, flickr_api_key):
    downloader = FlickrDownloader(flickr_api_key, download_folder)

    photo_list_result = downloader.get_photo_list()
    photo_list = photo_list_result["photos"]["photo"]

    requested_photo = [photo for photo in photo_list if photo["id"] == photo_id]

    photo_location = os.path.join(download_folder, "{}.jpg".format(photo_id))

    photo_content = downloader.download_photo(requested_photo)

    downloader.save_photo(photo_location, photo_content)

    return photo_location
