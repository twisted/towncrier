from __future__ import annotations

import abc

from typing import TYPE_CHECKING, Any, Iterable, Mapping


if TYPE_CHECKING:
    from .load import CategoryType, Config


class BaseFragmentTypesLoader:
    """Base class to load fragment types."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, config: Mapping[str, Any], parsed_config: Config):
        """Initialize."""
        self.config = config
        self.parsed_config = parsed_config

    @classmethod
    def factory(
        cls, config: Mapping[str, Any], parsed_config: Config
    ) -> BaseFragmentTypesLoader:
        fragment_types_class: type[BaseFragmentTypesLoader] = DefaultFragmentTypesLoader
        fragment_types = config.get("fragment", {})
        types_config = config.get("type", {})
        if fragment_types:
            fragment_types_class = TableFragmentTypesLoader
        elif types_config:
            fragment_types_class = ArrayFragmentTypesLoader

        new = fragment_types_class(config, parsed_config)
        return new

    @abc.abstractmethod
    def load(self) -> Mapping[str, CategoryType]:
        """Load fragment types."""


class DefaultFragmentTypesLoader(BaseFragmentTypesLoader):
    """Default towncrier's fragment types."""

    _default_types: Mapping[str, CategoryType] = {
        # Keep in-sync with docs/tutorial.rst.
        "feature": {"name": "Features", "showcontent": True, "check": True},
        "bugfix": {"name": "Bugfixes", "showcontent": True, "check": True},
        "doc": {"name": "Improved Documentation", "showcontent": True, "check": True},
        "removal": {
            "name": "Deprecations and Removals",
            "showcontent": True,
            "check": True,
        },
        "misc": {"name": "Misc", "showcontent": False, "check": True},
    }

    def load(self) -> Mapping[str, CategoryType]:
        """Load default types."""
        return self._default_types


class ArrayFragmentTypesLoader(BaseFragmentTypesLoader):
    """Load fragment types from an toml array of tables.

    This loader get the custom fragment types defined through a
    toml array of tables, that ``toml`` parses as an array
    of mappings.

    For example::

        [tool.towncrier]
        [[tool.towncrier.type]]
        directory = "deprecation"
        name = "Deprecations"
        showcontent = true

    """

    def load(self) -> Mapping[str, CategoryType]:
        """Load types from toml array of mappings."""

        types: dict[str, CategoryType] = {}
        types_config = self.config["type"]
        for type_config in types_config:
            fragment_type_name = type_config["name"]
            directory = type_config.get("directory", fragment_type_name.lower())
            is_content_required = type_config.get("showcontent", True)
            check = type_config.get("check", True)
            types[directory] = {
                "name": fragment_type_name,
                "showcontent": is_content_required,
                "check": check,
                "all_bullets": type_config.get(
                    "all_bullets", self.parsed_config.all_bullets
                ),
            }
        return types


class TableFragmentTypesLoader(BaseFragmentTypesLoader):
    """Load fragment types from toml tables.

    This loader get the custom fragment types defined through a
    toml  tables, that ``toml`` parses as an nested mapping.

    This loader allows omitting ``name`` and
    ```showcontent`` fields.
    ``name`` by default is the capitalized
    fragment type.
    ``showcontent`` is true by default.

    For example::

        [tool.towncrier]
        [tool.towncrier.fragment.chore]
        name = "Chores"
        showcontent = False

        [tool.towncrier.fragment.deprecations]
        # name will be "Deprecations"
        # The content will be shown.

    """

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize."""
        super().__init__(*args, **kwargs)
        self.fragment_options = self.config.get("fragment", {})

    def load(self) -> Mapping[str, CategoryType]:
        """Load types from nested mapping."""
        fragment_types: Iterable[str] = self.fragment_options.keys()
        fragment_types = sorted(fragment_types)
        custom_types_sequence = [
            (fragment_type, self._load_options(fragment_type))
            for fragment_type in fragment_types
        ]
        types = dict(custom_types_sequence)
        return types

    def _load_options(self, fragment_type: str) -> CategoryType:
        """Load fragment options."""
        capitalized_fragment_type = fragment_type.capitalize()
        options = self.fragment_options.get(fragment_type, {})
        fragment_description = options.get("name", capitalized_fragment_type)
        show_content = options.get("showcontent", True)
        check = options.get("check", True)
        clean_fragment_options: CategoryType = {
            "name": fragment_description,
            "showcontent": show_content,
            "check": check,
            "all_bullets": options.get("all_bullets", self.parsed_config.all_bullets),
        }
        return clean_fragment_options
