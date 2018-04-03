from setuptools import setup, find_packages


long_description = ""

setup(
    name="flickr_downloader",
    version="1.0.0",
    description="Python package that downloads 100 interesting photos from Flickr",
    long_description=long_description,
    author="Mihai Costea",
    author_email="mihai@mcostea.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    keywords="flickr photo downloader",
    packages=find_packages(),
    install_requires=["requests>=2"],
    python_requires="~=3"
)
