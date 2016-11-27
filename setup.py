"""
py2app build script for xmlChecker.

Will automatically ensure that all build prerequisites are available
via ez_setup.

Usage:
    python setup.py py2app
"""
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup
setup(
    app=["xmlChecker.py"],
setup_requires=["py2app"],
)