# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
Responsible for getting the version and name from a project.
"""


from __future__ import annotations

import importlib.metadata as importlib_metadata
import sys

from importlib import import_module
from types import ModuleType
from typing import Any


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
    version: Any

    module = _get_package(package_dir, package)
    version = getattr(module, "__version__", None)
    if not version:
        try:
            version = importlib_metadata.version(package)
        except importlib_metadata.PackageNotFoundError:
            raise Exception(f"Package not installed and no {package}.__version__ found")

    if isinstance(version, str):
        return version.strip()

    if isinstance(version, tuple):
        return ".".join(map(str, version)).strip()

    # Try duck-typing as an Incremental version.
    if hasattr(version, "base"):
        try:
            version = str(version.base()).strip()
            # Incremental uses `X.Y.rcN`.
            # Standardize on importlib (and PEP440) use of `X.YrcN`:
            return version.replace(".rc", "rc")  # type: ignore
        except TypeError:
            pass

    raise Exception(
        "Version must be a string, tuple, or an Incremental Version."
        " If you can't provide that, use the --version argument and specify one."
    )


def get_project_name(package_dir: str, package: str) -> str:
    module = _get_package(package_dir, package)
    version = getattr(module, "__version__", None)
    # Incremental has support for package names, try duck-typing it.
    try:
        return str(version.package)  # type: ignore
    except AttributeError:
        pass

    return package.title()
