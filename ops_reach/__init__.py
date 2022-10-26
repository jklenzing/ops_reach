"""Core library for ops_reach.

This is a library of `pysat` instrument modules and methods designed to support
REACH instruments for conversion of level 1b data to level 1c.

"""

import os
from ops_reach import instruments  # noqa F401

# set version
__here__ = os.path.abspath(os.path.dirname(__file__))
version_filename = os.path.join(__here__, 'version.txt')
with open(version_filename, 'r') as version_file:
    __version__ = version_file.read().strip()

del version_filename, version_file
