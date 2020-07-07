#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

CONFIG = generate_distutils_setup(
    packages=['ackermann_twist_joy'],
    package_dir={'': 'src'}
)

setup(**CONFIG)
