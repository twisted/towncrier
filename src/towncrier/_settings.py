# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
import toml

from collections import OrderedDict


class ConfigError(Exception):
    def __init__(self, *args, **kwargs):
        self.failing_option = kwargs.get("failing_option")
        super().__init__(*args, **kwargs)


_start_string = u".. towncrier release notes start\n"
_title_format = None
_template_fname = None
_default_types = OrderedDict(
    [
        (u"feature", {"name": u"Features", "showcontent": True}),
        (u"bugfix", {"name": u"Bugfixes", "showcontent": True}),
        (u"doc", {"name": u"Improved Documentation", "showcontent": True}),
        (u"removal", {"name": u"Deprecations and Removals", "showcontent": True}),
        (u"misc", {"name": u"Misc", "showcontent": False}),
    ]
)
_underlines = ["=", "-", "~"]


def load_config(directory):
    return load_config_from_file(os.path.join(directory, "pyproject.toml"))


def load_config_from_file(from_file):
    if not os.path.exists(from_file):
        config = {"tool": {"towncrier": {}}}
    else:
        with open(from_file, "r") as conffile:
            config = toml.load(conffile)

    return parse_toml(config)


def parse_toml(config):
    if "tool" not in config:
        raise ConfigError("No [tool.towncrier] section.", failing_option="all")

    config = config["tool"]["towncrier"]

    sections = OrderedDict()
    types = OrderedDict()

    if "section" in config:
        for x in config["section"]:
            sections[x.get("name", "")] = x["path"]
    else:
        sections[""] = ""

    if "type" in config:
        for x in config["type"]:
            types[x["directory"]] = {"name": x["name"], "showcontent": x["showcontent"]}
    else:
        types = _default_types

    wrap = config.get("wrap", False)

    single_file_wrong = config.get("singlefile")
    if single_file_wrong:
        raise ConfigError(
            "`singlefile` is not a valid option. Did you mean `single_file`?",
            failing_option="singlefile",
        )

    single_file = config.get("single_file", True)
    if not isinstance(single_file, bool):
        raise ConfigError(
            "`single_file` option must be a boolean: false or true.",
            failing_option="single_file",
        )

    return {
        "package": config.get("package", ""),
        "package_dir": config.get("package_dir", "."),
        "single_file": single_file,
        "filename": config.get("filename", "NEWS.rst"),
        "directory": config.get("directory"),
        "sections": sections,
        "types": types,
        "template": config.get("template", _template_fname),
        "start_line": config.get("start_string", _start_string),
        "title_format": config.get("title_format", _title_format),
        "issue_format": config.get("issue_format"),
        "underlines": config.get("underlines", _underlines),
        "wrap": wrap,
    }
