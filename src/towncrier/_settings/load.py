# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import annotations

import atexit
import dataclasses
import os
import re
import sys

from contextlib import ExitStack
from pathlib import Path
from typing import Any, Literal, Mapping, Sequence

from click import ClickException

from .._settings import fragment_types as ft


if sys.version_info < (3, 10):
    import importlib_resources as resources
else:
    from importlib import resources


if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib


re_resource_template = re.compile(r"[-\w.]+:[-\w.]+$")


@dataclasses.dataclass
class Config:
    sections: Mapping[str, str]
    types: Mapping[str, Mapping[str, Any]]
    template: str | tuple[str, str]
    start_string: str
    package: str = ""
    package_dir: str = "."
    single_file: bool = True
    filename: str = "NEWS.rst"
    directory: str | None = None
    version: str | None = None
    name: str = ""
    title_format: str | Literal[False] = ""
    issue_format: str | None = None
    underlines: Sequence[str] = ("=", "-", "~")
    wrap: bool = False
    all_bullets: bool = True
    orphan_prefix: str = "+"


class ConfigError(ClickException):
    def __init__(self, *args: str, **kwargs: str):
        self.failing_option = kwargs.get("failing_option")
        super().__init__(*args)


def load_config_from_options(
    directory: str | None, config_path: str | None
) -> tuple[str, Config]:
    if config_path is None:
        if directory is None:
            directory = os.getcwd()

        base_directory = os.path.abspath(directory)
        config = load_config(base_directory)
    else:
        config_path = os.path.abspath(config_path)
        if directory is None:
            base_directory = os.path.dirname(config_path)
        else:
            base_directory = os.path.abspath(directory)
        config = load_config_from_file(os.path.dirname(config_path), config_path)

    if config is None:
        raise ConfigError(f"No configuration file found.\nLooked in: {base_directory}")

    return base_directory, config


def load_config(directory: str) -> Config | None:
    towncrier_toml = os.path.join(directory, "towncrier.toml")
    pyproject_toml = os.path.join(directory, "pyproject.toml")

    if os.path.exists(towncrier_toml):
        config_file = towncrier_toml
    elif os.path.exists(pyproject_toml):
        config_file = pyproject_toml
    else:
        return None

    return load_config_from_file(directory, config_file)


def load_config_from_file(directory: str, config_file: str) -> Config:
    with open(config_file, "rb") as conffile:
        config = tomllib.load(conffile)

    return parse_toml(directory, config)


# Clean up possible temporary files on exit.
_file_manager = ExitStack()
atexit.register(_file_manager.close)


def parse_toml(base_path: str, config: Mapping[str, Any]) -> Config:
    if "towncrier" not in (config.get("tool") or {}):
        raise ConfigError("No [tool.towncrier] section.", failing_option="all")

    config = config["tool"]["towncrier"]
    parsed_data = {}

    # Check for misspelt options.
    for typo, correct in [
        ("singlefile", "single_file"),
    ]:
        if config.get(typo):
            raise ConfigError(
                f"`{typo}` is not a valid option. Did you mean `{correct}`?",
                failing_option=typo,
            )

    # Process options.
    for field in dataclasses.fields(Config):
        if field.name in ("sections", "types", "template"):
            # Skip these options, they are processed later.
            continue
        if field.name in config:
            #  Interestingly, the __future__ annotation turns the type into a string.
            if field.type in ("bool", bool):
                if not isinstance(config[field.name], bool):
                    raise ConfigError(
                        f"`{field.name}` option must be boolean: false or true.",
                        failing_option=field.name,
                    )
            parsed_data[field.name] = config[field.name]

    # Process 'section'.
    sections = {}
    if "section" in config:
        for x in config["section"]:
            sections[x.get("name", "")] = x["path"]
    else:
        sections[""] = ""
    parsed_data["sections"] = sections

    # Process 'types'.
    fragment_types_loader = ft.BaseFragmentTypesLoader.factory(config)
    parsed_data["types"] = fragment_types_loader.load()

    # Process 'template'.
    markdown_file = Path(config.get("filename", "")).suffix == ".md"
    template = config.get("template", "towncrier:default")
    if re_resource_template.match(template):
        package, resource = template.split(":", 1)
        if not Path(resource).suffix:
            resource += ".md" if markdown_file else ".rst"

        if not _pkg_file_exists(package, resource):
            if _pkg_file_exists(package + ".templates", resource):
                package += ".templates"
            else:
                raise ConfigError(
                    f"'{package}' does not have a template named '{resource}'.",
                    failing_option="template",
                )
        template = (package, resource)
    else:
        template = os.path.join(base_path, template)
        if not os.path.isfile(template):
            raise ConfigError(
                f"The template file '{template}' does not exist.",
                failing_option="template",
            )

    parsed_data["template"] = template

    # Process 'start_string'.

    start_string = config.get("start_string", "")
    if not start_string:
        start_string_template = "<!-- {} -->\n" if markdown_file else ".. {}\n"
        start_string = start_string_template.format("towncrier release notes start")
    parsed_data["start_string"] = start_string

    # Return the parsed config.
    return Config(**parsed_data)


def _pkg_file_exists(pkg: str, file: str) -> bool:
    """
    Check whether *file* exists within *pkg*.
    """
    return resources.files(pkg).joinpath(file).is_file()
