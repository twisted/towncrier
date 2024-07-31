"""
Provides towncrier version information.
"""

# For dev   - 23.11.0.dev0
# For RC    - 23.11.0rc1  (release candidate starts at 1)
# For final - 23.11.0
# make sure to follow PEP440
__version__ = "24.7.0"

_hatchling_version = __version__
__all__ = ["_hatchling_version"]
