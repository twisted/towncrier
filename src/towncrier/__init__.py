# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
towncrier, a builder for your news files.
"""

from __future__ import annotations

from incremental import Version


__all__ = ["__version__"]


def __getattr__(name: str) -> Version:
    if name != "__version__":
        raise AttributeError(f"module {__name__} has no attribute {name}")

    import warnings

    from ._version import __version__

    warnings.warn(
        "Accessing towncrier.__version__ is deprecated and will be "
        "removed in a future release. Use importlib.metadata directly "
        "to query for towncrier's packaging metadata.",
        DeprecationWarning,
        stacklevel=2,
    )

    return __version__
