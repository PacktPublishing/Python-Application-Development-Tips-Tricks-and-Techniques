import os
from histogram import *


if __name__ == "__main__":
    # Photo source: https://commons.wikimedia.org/wiki/File:Nature-View.jpg
    print([int(i) for i in calculate_histogram(os.path.join(os.path.realpath(os.path.dirname(__file__)), "Nature-View.jpg"))])

