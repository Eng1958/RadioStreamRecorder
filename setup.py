#!/usr/bin/env python3
# Usage: setup.py build

# See:  https://github.com/kennethreitz/setup.py A Human's Ultimate Guide to
#       setup.py

"""
    Usage: setup.py build

    See:  https://github.com/kennethreitz/setup.py A Human's Ultimate Guide to
        setup.py

"""
import io
import os
from distutils.core import setup

# Package meta-data.
NAME = 'RadioStreamRecorder'
DESCRIPTION = 'Record inernet radio'
URL = 'https://github.com/Eng1958/RadioStreamRecorder'
EMAIL = 'dieter@engemann.me'
AUTHOR = 'Dieter Engemann'


HERE = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in
# file!
with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
ABOUT = {}
with open(os.path.join(HERE, NAME, '__version__.py')) as f:
    exec(f.read(), ABOUT)


# where the magic happens
setup(
    name=NAME,
    version=ABOUT['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    packages=['RadioStreamRecorder'],

    # The project's main homepage.
    url=URL,
    ## py_modules=['RadioStreamRecorder',
    ##             'rsrhelper'],
    platforms=["Linux"],
    classifiers=["Development Status :: 4 - Beta",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                ],
    scripts=['bin/RadioStreamRecorder']

    )
