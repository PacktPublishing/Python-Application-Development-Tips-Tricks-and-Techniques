import cv2
import numpy
import os


def calculate_histogram(photo_):
    bins = numpy.zeros(256, numpy.int32)

    for i in range(photo_.shape[0]):
        for j in range(photo_.shape[1]):
            intensity = sum(photo_[i][j])
            bins[int(intensity/3)] += 1

    return bins


if __name__ == "__main__":
    # Photo source: https://commons.wikimedia.org/wiki/File:Nature-View.jpg
    photo = cv2.imread(os.path.join(os.path.realpath(os.path.dirname(__file__)), "Nature-View.jpg"))
    histogram = calculate_histogram(photo)
    print(histogram)
