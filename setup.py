#!/usr/bin/env python

from distutils.core import setup

setup(name='tumbleweed',
      version='0.1',
      description='A framework for creating tumblelogs from information denormalized in haystack.',
      author='Matt Croydon',
      author_email='mcroydon@gmail.com',
      url='http://postneo.com/',
      packages=['tumbleweed', 'tumbleweed.templatetags'],
      package_dir={'tumbleweed': 'tumbleweed'},
     )
