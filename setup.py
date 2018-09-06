#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

from setuptools import setup, find_packages

setup(
    name='towncrier',
    maintainer='Amber Brown',
    maintainer_email='hawkowl@twistedmatrix.com',
    url="https://github.com/hawkowl/towncrier",
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    use_incremental=True,
    setup_requires=['incremental'],
    install_requires=[
        'Click',
        'incremental',
        'jinja2',
        'toml',
    ],
    package_dir={"": "src"},
    packages=find_packages('src'),
    license="MIT",
    zip_safe=False,
    include_package_data=True,
    description='Building newsfiles for your project.',
    long_description=open('README.rst').read(),
    entry_points={
        'console_scripts': [
            'towncrier = towncrier:_main',
        ],
    }
)
