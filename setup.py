import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "apilight",
    version = "0.0.4",
    author = "Toma Dragos",
    author_email = "tomadragos96@gmail.com",
    description = ("help funcs and utilities"),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://...",
    packages=['apilight'],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
