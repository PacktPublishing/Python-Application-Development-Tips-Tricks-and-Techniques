# Flickr Downloader

Flickr Downloader is a small Python package that can be used to download 100 interesting photos from Flickr.


## Installation

```
$ pip install flickr_downloader
```

## Usage

This package requires a valid Flickr API Key. You can get one from [Flickr Developer Guide](https://www.flickr.com/services/developer/api/)


```
from flickr_downloader import download_interesting_photos


flickr_api_key = ...
location = ... # Download folder must already exist

download_interesting_photos(flickr_api_key, location)
```

## License
Flickr Downloader is released under the MIT license. See LICENSE for details.

## Contact
Follow me on twitter [@mcostea](https://twitter.com/mcostea)
