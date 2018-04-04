import os
from flickr_downloader.flickr_downloader import download_interesting_photos


if __name__ == "__main__":
    if not os.path.exists("downloaded"):
        os.mkdir("downloaded")
    download_interesting_photos(os.environ["FLICKR_API_KEY"], "downloaded")
