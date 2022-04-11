# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os

from collections import OrderedDict

import pkg_resources
import tomli

from .._settings import fragment_types as ft


class ConfigError(Exception):
    def __init__(self, *args, **kwargs):
        self.failing_option = kwargs.get("failing_option")
        super().__init__(*args)


_start_string = ".. towncrier release notes start\n"
_title_format = None
_template_fname = "towncrier:default"
_underlines = ["=", "-", "~"]


def load_config_from_options(directory, config):
    if config is None:
        if directory is None:
            directory = os.getcwd()

        base_directory = os.path.abspath(directory)
        config = load_config(base_directory)
    else:
        config = os.path.abspath(config)
        if directory:
            base_directory = os.path.abspath(directory)
        else:
            base_directory = os.path.dirname(config)
        config = load_config_from_file(os.path.dirname(config), config)

    if config is None:
        raise ConfigError(f"No configuration file found.\nLooked in: {base_directory}")

    return base_directory, config


def load_config(directory):

    towncrier_toml = os.path.join(directory, "towncrier.toml")
    pyproject_toml = os.path.join(directory, "pyproject.toml")

    if os.path.exists(towncrier_toml):
        config_file = towncrier_toml
    elif os.path.exists(pyproject_toml):
        config_file = pyproject_toml
    else:
        return None

    return load_config_from_file(directory, config_file)


def load_config_from_file(directory, config_file):
    with open(config_file, "rb") as conffile:
        config = tomli.load(conffile)

    return parse_toml(directory, config)


def parse_toml(base_path, config):
    if "tool" not in config:
        raise ConfigError("No [tool.towncrier] section.", failing_option="all")

    config = config["tool"]["towncrier"]

    sections = OrderedDict()
    if "section" in config:
        for x in config["section"]:
            sections[x.get("name", "")] = x["path"]
    else:
        sections[""] = ""
    fragment_types_loader = ft.BaseFragmentTypesLoader.factory(config)
    types = fragment_types_loader.load()

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

    all_bullets = config.get("all_bullets", True)
    if not isinstance(all_bullets, bool):
        raise ConfigError(
            "`all_bullets` option must be boolean: false or true.",
            failing_option="all_bullets",
        )

    template = config.get("template", _template_fname)
    if template.startswith("towncrier:"):
        resource_name = "templates/" + template.split("towncrier:", 1)[1] + ".rst"
        if not pkg_resources.resource_exists("towncrier", resource_name):
            raise ConfigError(
                "Towncrier does not have a template named '%s'."
                % (template.split("towncrier:", 1)[1],)
            )

        template = pkg_resources.resource_filename("towncrier", resource_name)
    else:
        template = os.path.join(base_path, template)

    if not os.path.exists(template):
        raise ConfigError(
            f"The template file '{template}' does not exist.",
            failing_option="template",
        )

    return {
        "package": config.get("package", ""),
        "package_dir": config.get("package_dir", "."),
        "single_file": single_file,
        "filename": config.get("filename", "NEWS.rst"),
        "directory": config.get("directory"),
        "version": config.get("version"),
        "name": config.get("name"),
        "sections": sections,
        "types": types,
        "template": template,
        "start_string": config.get("start_string", _start_string),
        "title_format": config.get("title_format", _title_format),
        "issue_format": config.get("issue_format"),
        "underlines": config.get("underlines", _underlines),
        "wrap": wrap,
        "all_bullets": all_bullets,
    }
