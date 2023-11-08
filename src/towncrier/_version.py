"""
Provides towncrier version information.
"""

# This file is auto-generated! Do not edit!
# Use `python -m incremental.update towncrier` to change this file.

from incremental import Version


# For dev   - Version('towncrier', 23, 8, 1, dev=0)
# For RC    - Version('towncrier', 23, 9, 0, release_candidate=1)
# For final - Version('towncrier', 23, 9, 0)
__version__ = Version("towncrier", 23, 11, 0)
# The version is exposed in string format to be
# available for the hatching build tools.
_hatchling_version = __version__.short()

__all__ = ["__version__", "_hatchling_version"]
