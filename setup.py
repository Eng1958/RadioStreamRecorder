#!/usr/bin/env python3
# Usage: setup.py build

# See:  https://github.com/kennethreitz/setup.py A Human's Ultimate Guide to
#       setup.py

import io
import os
from distutils.core import setup


# Package meta-data.
NAME = 'package'
DESCRIPTION = 'Record inernet radio'
URL = 'https://github.com/Eng1958/RadioStreamRecorder'
EMAIL = 'dieter@engemann.me'
AUTHOR = 'Dieter Engemann'


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in
# file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)


# where the magic happens
setup( 
    name = NAME, 
    version = about['__version__'],
    description = DESCRIPTION,
    long_description = long_description,
    author = AUTHOR, 
    author_email = EMAIL, 
    maintainer = AUTHOR,
    maintainer_email=EMAIL,

    # The project's main homepage.
    url=URL,

    py_modules = ['RadioStreamRecorder',
                  'rsrhelper'],
    )
