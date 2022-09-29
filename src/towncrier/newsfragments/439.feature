We now have easy markdown-compatible rendering!

When the configured filename has a ``.md`` extension: the title, sections, and
newsfragment categories are output respectively with #, ## and ### markdown
headings prefixed (and without any underlines). Bulleted issues are also
indented, with multi-line spaces between to rendered correctly with Python's
standard markdown implementation.

The default template no longer renders an empty newline for empty underlines
configurations, and templates are rendered with extra context for ``bullet``,
``title_prefix``, ``section_prefix``, and ``category_prefix``.
