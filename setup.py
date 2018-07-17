from distutils.core import setup
import sys

if not ((3, 5, 0) <= sys.version_info < (3, 6, 0)):
    sys.exit('Only python 3.5.* is supported.')

setup(
    name='autoextractor',
    version='0.1.0',
    packages=['autoextractor'],
    long_description='Extract and transform data for model training',
)
