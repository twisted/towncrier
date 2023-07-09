"""
Provides towncrier version information.
"""

from importlib.metadata import PackageNotFoundError, version


try:
    _version = version("towncrier")
except PackageNotFoundError:  # pragma: no cover
    _version = "0.0.0.dev"

_hatchling_version = _version
__all__ = ["_hatchling_version"]
