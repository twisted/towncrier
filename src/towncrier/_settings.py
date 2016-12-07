# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
import toml

from collections import OrderedDict

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


_start_string = '.. towncrier release notes start\n'
_title_format = '{name} {version}\n==========\n'
_template_fname = None
_default_types = OrderedDict([
    (u"feature", {"name": u"Features", "showcontent": True}),
    (u"bugfix", {"name": u"Bugfixes", "showcontent": True}),
    (u"doc", {"name": u"Improved Documentation", "showcontent": True}),
    (u"removal", {"name": u"Deprecations and Removals",
                  "showcontent": True}),
    (u"misc", {"name": u"Misc", "showcontent": False}),
])


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

    try:
        start_string = config.get('towncrier', 'start_string')
    except configparser.NoOptionError:
        start_string = _start_string

    try:
        title_format = config.get('towncrier', 'title_format')
    except configparser.NoOptionError:
        title_format = _title_format

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
        'types': _default_types,
        'template': template_fname,
        'start_line': start_string,
        'title_format': title_format,
    }


def load_config_toml(from_dir):
    fn = os.path.join(from_dir, "pyproject.toml")
    if not os.path.exists(fn):
        return None
    with open(fn, 'r') as conffile:
        config = toml.load(conffile)

    if 'tool' not in config:
        raise ValueError("No [tool.towncrier] section.")

    config = config['tool']['towncrier']

    if 'package' not in config:
        raise ValueError(
            "The [tool.towncrier] section has no required 'package' key.")

    sections = OrderedDict()
    types = OrderedDict()

    if "section" in config:
        for x in config["section"]:
            sections[x.get('name', '')] = x['path']
    else:
        sections[''] = ''

    if "type" in config:
        for x in config["type"]:
            types[x["directory"]] = {"name": x["name"],
                                     "showcontent": x["showcontent"]}
    else:
        types = _default_types

    return {
        'package': config.get('package'),
        'package_dir': config.get('package_dir', '.'),
        'filename': config.get('filename', 'NEWS.rst'),
        'directory': config.get('directory'),
        'sections': sections,
        'types': types,
        'template': config.get('template', _template_fname),
        'start_line': config.get('start_string', _start_string),
        'title_format': config.get('title_format', _title_format),
    }


def load_config(from_dir):
    res = load_config_toml(from_dir)
    if res is None:
        return load_config_ini(from_dir)
    return res
