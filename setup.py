import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="python-pushbullet",
    version="1.0.0",
    description="A python module for interacting with the v2 Pushbullet API.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dylan-robins/python-pushbullet",
    author="Dylan Robins",
    author_email="dylan.robins@gmail.com",
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=["pushbullet"],
    include_package_data=True,
    install_requires=["requests==2.26.0", "python-dotenv==0.19.0"],
    entry_points={
        "console_scripts": [
            "pushbullet=pushbullet.__main__:main",
        ]
    },
)
