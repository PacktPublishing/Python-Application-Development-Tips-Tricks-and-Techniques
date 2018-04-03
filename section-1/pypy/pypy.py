import os
from PIL import Image


def calculate_histogram(photo_):
    bins = []
    for i in range(256):
        bins.append(0)
    
    width, height = photo_.size

    for i in range(width):
        for j in range(height):
            intensity = sum(photo.getpixel((i, j)))
            bins[int(intensity/3)] += 1

    return bins


if __name__ == "__main__":
    # Photo source: https://commons.wikimedia.org/wiki/File:Nature-View.jpg
    photo = Image.open(os.path.join(os.path.realpath(os.path.dirname(__file__)), "Nature-View.jpg"))
    histogram = calculate_histogram(photo)
    print(histogram)
