# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
import toml

from collections import OrderedDict

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def load_config_ini(from_dir):

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
        'types': OrderedDict([
            ("feature", {"name": "Features", "showcontent": True}),
            ("bugfix", {"name": "Bugfixes", "showcontent": True}),
            ("doc", {"name": "Improved Documentation", "showcontent": True}),
            ("removal", {"name": "Deprecations and Removals",
                         "showcontent": True}),
            ("misc", {"name": "Misc", "showcontent": False}),
        ])
    }

def load_config_toml(from_dir):

    with open(os.path.join(from_dir, "pyproject.toml"), 'r') as conffile:
        config = toml.loads(conffile.read())

    if 'tool' not in config:
        raise ValueError("No [tool.towncrier] section.")

    config = config['tool']['towncrier']

    if 'package' not in config:
        raise ValueError(
            "The [towncrier] section has no required 'package' key.")

    sections = OrderedDict()
    types = OrderedDict()

    for x in config["section"]:
        sections[x.get('name', '')] = x['path']

    for x in config["type"]:
        types[x["directory"]] = {"name": x["name"], "showcontent": x["showcontent"]}

    return {
        'package': config.get('package'),
        'package_dir': config.get('package_dir'),
        'filename': config.get('filename'),
        'directory': config.get('directory'),
        'sections': sections,
        'types': types,
    }

def load_config(from_dir):
    try:
        return load_config_toml(from_dir)
    except:
        return load_config_ini(from_dir)
