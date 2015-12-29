# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os

import configparser


def load_config(from_dir):

    config = configparser.ConfigParser()
    config.read(os.path.join(from_dir, "towncrier.ini"))

    if 'towncrier' not in config.sections():
        raise ValueError("No [towncrier] section.")

    if 'package' not in config['towncrier']:
        raise ValueError(
            "The [towncrier] section has no required 'package' key.")

    return {
        'package': config['towncrier']['package'],
        'package_dir': config['towncrier'].get('package_dir', '.'),
        'filename': config['towncrier'].get('filename', 'NEWS.rst'),
        'sections': {'': ''},
    }
