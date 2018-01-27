# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
import toml

from collections import OrderedDict


_start_string = u'.. towncrier release notes start\n'
_title_format = u'{name} {version} ({project_date})'
_template_fname = None
_default_types = OrderedDict([
    (u"feature", {"name": u"Features", "showcontent": True}),
    (u"bugfix", {"name": u"Bugfixes", "showcontent": True}),
    (u"doc", {"name": u"Improved Documentation", "showcontent": True}),
    (u"removal", {"name": u"Deprecations and Removals",
                  "showcontent": True}),
    (u"misc", {"name": u"Misc", "showcontent": False}),
])
_underlines = ["=", "-", "~"]


def load_config(from_dir):
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
    if "section" in config:
        for x in config["section"]:
            sections[x.get('name', '')] = x['path']
    else:
        sections[''] = ''

    types = OrderedDict()
    if "type" in config:
        for x in config["type"]:
            types[x["directory"]] = {
                "name": x["name"], "showcontent": x["showcontent"]}
    else:
        types = _default_types

    formats = OrderedDict()
    if "format" in config:
        for x in config["format"]:
            formats[x["kind"]] = {
                "patterns": x["patterns"], "format": x["format"]}
    else:
        # backwards compatibility
        issue_format = config.get('issue_format')
        if issue_format:
            issue_format = issue_format.replace('{issue}', '{id}')
            formats["old-issue-format"] = {
                "patterns": [".*"], "format": issue_format}

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
        'formats': formats,
        'underlines': config.get('underlines', _underlines)
    }
