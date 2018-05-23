from setuptools import setup, find_packages


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="flickr_downloader",
    version="1.0.0-dev2",
    description="Python package that downloads 100 interesting photos from Flickr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mihai Costea",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    keywords="flickr photo downloader",
    packages=find_packages(),
    install_requires=["requests>=2"],
    python_requires="~=3.5"
)
