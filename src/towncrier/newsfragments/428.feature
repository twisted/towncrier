You can now create fragments that are not associated with issues. Start the name of the fragment with ``+`` (e.g. ``+anything.feature``).
The content of these orphan news fragments will be included in the release notes, at the end of the category corresponding to the file extension.

To help quickly create a unique orphan news fragment, ``towncrier create +.feature`` will append a random string to the base name of the file, to avoid name collisions.
