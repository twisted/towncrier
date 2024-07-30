"""
Provides towncrier version information.
"""

# For dev   - 23.11.1.dev0
# For RC    - 23.11.1.rc1
# For final - 23.11.1
# make sure to follow PEP440
__version__ = "23.11.1.dev0"

_hatchling_version = __version__
__all__ = ["_hatchling_version"]
