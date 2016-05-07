# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def load_config(from_dir):

    config = configparser.ConfigParser(
        {
            'package_dir': '.',
            'filename': 'NEWS.rst',
            'directory': None,
        }
    )
    config.read(os.path.join(from_dir, "towncrier.ini"))

    if 'towncrier' not in config.sections():
        raise ValueError("No [towncrier] section.")

    if 'package' not in config.options('towncrier'):
        raise ValueError(
            "The [towncrier] section has no required 'package' key.")

    try:
        start_string = config.get('towncrier', 'start_string')
    except configparser.NoOptionError:
        start_string = '.. towncrier release notes start\n'

    try:
        title_format = config.get('towncrier', 'title_format')
    except configparser.NoOptionError:
        title_format = '{name} {version}\n==========\n'

    try:
        template_fname = config.get('towncrier', 'template')
    except configparser.NoOptionError:
        template_fname = None

    return {
        'package': config.get('towncrier', 'package'),
        'package_dir': config.get('towncrier', 'package_dir'),
        'filename': config.get('towncrier', 'filename'),
        'directory': config.get('towncrier', 'directory'),
        'sections': {'': ''},
        'template': template_fname,
        'start_string': start_string,
        'title_format': title_format,
    }
