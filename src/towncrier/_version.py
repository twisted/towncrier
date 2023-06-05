"""
Provides towncrier version information.
"""

# This file is auto-generated! Do not edit!
# Use `python -m incremental.update towncrier` to change this file.

from incremental import Version


__version__ = Version("towncrier", 23, 6, 0, release_candidate=1)
# The version is exposed in string format to be
# available for the hatching build tools.
_hatchling_version = __version__.short()

__all__ = ["__version__", "_hatchling_version"]
