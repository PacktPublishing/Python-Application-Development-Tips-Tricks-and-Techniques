import os
import numpy
from setuptools import setup, Extension

setup(
        name = "histogram_wrapper",
        version = "1.0.0",
        ext_modules = [Extension("histogram",
            ["src/histogram.cpp", "src/opencv_histogram.cpp"],
            libraries=["opencv_core", "opencv_imgproc", "opencv_imgcodecs"],
            include_dirs=[numpy.get_include(),
                os.path.dirname(os.path.realpath(__file__)) + "/include"])]
)
