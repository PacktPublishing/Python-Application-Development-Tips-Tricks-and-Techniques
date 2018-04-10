# You need PyGObject to run this application
# See install instructions at https://pygobject.readthedocs.io/en/latest/getting_started.html

import gi
import os
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from flickr_downloader.flickr_downloader import download_interesting_photos


def download_button_clicked(sender):
    write_path = os.path.join(os.path.expanduser("~"), "downloaded_photos")
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    download_interesting_photos(os.environ["FLICKR_API_KEY"], write_path)


window = Gtk.Window(title="Hello World")

button = Gtk.Button(label="Download Photos")

window.add(button)

button.connect("clicked", download_button_clicked)

window.show_all()
window.connect("destroy", Gtk.main_quit)
Gtk.main()
