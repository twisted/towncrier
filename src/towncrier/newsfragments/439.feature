We now have easy markdown-compatible rendering!

When the configured filename has a ``.md`` extension, the default value of
``underlines`` and (the new) ``title_prefixes`` configuration values are
changed to ``["", "", ""]`` and ``["# ", "## ", "###"]``, respectively.

The default template no longer renders an empty line for empty underlines
configurations, and templates are rendered with extra context for
``title_prefix``, ``section_prefix``, and ``category_prefix.