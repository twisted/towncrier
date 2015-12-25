#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import os, sys

from setuptools import setup, find_packages

setup(
    name='towncrier',
    maintainer='Amber Brown',
    maintainer_email='hawkowl@twistedmatrix.com',
    url="https://github.com/hawkowl/towncrier",
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    use_incremental=True,
    setup_requires=['incremental'],
    install_requires=[
        'Click',
    ],
    package_dir={"": "src"},
    packages=find_packages('src'),
    license="MIT",
    zip_safe=False,
    long_description=open('README.rst').read(),
    entry_points={
        'console_scripts': [
            'towncrier = towncrier:_main',
        ],
    }
)
