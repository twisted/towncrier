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

    return {
        'package': config.get('towncrier', 'package'),
        'package_dir': config.get('towncrier', 'package_dir'),
        'filename': config.get('towncrier', 'filename'),
        'directory': config.get('towncrier', 'directory'),
        'sections': {'': ''},
    }
