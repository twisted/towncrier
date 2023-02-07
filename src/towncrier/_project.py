# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
Responsible for getting the version and name from a project.
"""


from __future__ import annotations

import sys

from importlib import import_module
from types import ModuleType

from incremental import Version as IncrementalVersion


def _get_package(package_dir: str, package: str) -> ModuleType:
    try:
        module = import_module(package)
    except ImportError:
        # Package is not already available / installed.
        # Force importing it based on the source files.
        sys.path.insert(0, package_dir)

        try:
            module = import_module(package)
        except ImportError as e:
            err = f"tried to import {package}, but ran into this error: {e}"
            # NOTE: this might be redirected via "towncrier --draft > …".
            print(f"ERROR: {err}")
            raise
        finally:
            sys.path.pop(0)

    return module


def get_version(package_dir: str, package: str) -> str:
    module = _get_package(package_dir, package)

    version = getattr(module, "__version__", None)

    if not version:
        raise Exception("No __version__, I don't know how else to look")

    if isinstance(version, str):
        return version.strip()

    if isinstance(version, IncrementalVersion):
        # FIXME:https://github.com/twisted/incremental/issues/81
        # Incremental uses `.rcN`.
        # importlib uses `rcN` (without a dot separation).
        # Here we make incremental work like importlib.
        return version.base().strip().replace(".rc", "rc")

    if isinstance(version, tuple):
        return ".".join(map(str, version)).strip()

    raise Exception(
        "I only know how to look at a __version__ that is a str, "
        "an Increment Version, or a tuple. If you can't provide "
        "that, use the --version argument and specify one."
    )


def get_project_name(package_dir: str, package: str) -> str:
    module = _get_package(package_dir, package)

    version = getattr(module, "__version__", None)

    if not version:
        # welp idk
        return package.title()

    if isinstance(version, str):
        return package.title()

    if isinstance(version, IncrementalVersion):
        # Incremental has support for package names
        return version.package

    raise TypeError(f"Unsupported type for __version__: {type(version)}")
