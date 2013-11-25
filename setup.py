# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from pyramid_restpike import __version__

setup(name='pyramid_restpike',
      version=__version__,
      license='MIT',
      install_requires=[line for line in open('requirements.txt')],
      )
