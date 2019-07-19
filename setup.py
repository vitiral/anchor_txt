#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
  name = 'anchor_txt',
  packages = ['anchor_txt'],
  version = '0.1.1',
  license='MIT or APACHE-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'attributes in markdown',
  long_description=read('README.md'),
  author = 'Rett Berg',
  author_email = 'googberg@gmail.com',
  url = 'https://github.com/vitiral/anchor_txt',
  include_package_data=True,
  zip_safe=False,
  classifiers=[
      # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Operating System :: Unix',
      'Operating System :: POSIX',
      'Operating System :: Microsoft :: Windows',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: Implementation :: CPython',
      'Programming Language :: Python :: Implementation :: PyPy',
      'Topic :: Utilities',
  ],
    project_urls={
        'Documentation': 'https://anchor_txt.readthedocs.io/',
        'Changelog': 'https://anchor_txt.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/vitiral/anchor_txt/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=2.7, >=3.0',
    install_requires=read('requirements.txt').split('\n'),
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        # 'console_scripts': [
        #     'nameless = nameless.cli:main',
        # ]
    },
)
