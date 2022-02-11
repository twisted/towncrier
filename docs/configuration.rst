Configuration Reference
=======================

``towncrier`` has many knobs and switches you can use, to customise it to your project's needs.
The setup in the `Quick Start <quickstart.html>`_ doesn't touch on many, but this document will detail each of these options for you!

For how to perform common customisation tasks, see `Customisation <customisation/index.html>`_.

``[tool.towncrier]``
--------------------

All configuration for ``towncrier`` sits inside ``pyproject.toml``, under the ``tool.towncrier`` namespace.
Please see `the TOML GitHub repo <https://github.com/toml-lang/toml>`_ for how to write TOML.

Top level keys
~~~~~~~~~~~~~~

- ``package`` -- The package name of your project. (Python projects only)
- ``package_dir`` -- The folder your package lives. ``./`` by default, some projects might need to use ``src``. (Python projects only)
- ``newsfile`` -- The filename of your news file. ``NEWS.rst`` by default.
- ``fragment_directory`` -- If you are not storing your newsfragments in your Python package, or aren't using Python, this is the path to where your newsfragments will be put.
- ``template`` -- Path to an alternate template for generating the newsfile, if you have one.
- ``start_line`` -- The magic string that ``towncrier`` looks for when considering where the release notes should start. ``.. towncrier release notes start`` by default.
- ``title_format`` -- A format string for the title of your project. ``{name} {version} ({project_date})`` by default.
- ``issue_format`` -- A format string for rendering the issue/ticket number in newsfiles. ``#{issue}`` by default.
- ``underlines`` -- The characters used for underlining headers. ``["=", "-", "~"]`` by default.


Custom fragment types
---------------------

Custom fragment types can be including in the
pyproject.toml.
Each custom type (``[[tool.towncrier.type]]``) has the following keys:
 * ``directory``: The type of the fragment.
 * ``name``: The description of the fragment type, as it must be included
   in the news file.
 * ``showcontent``: Whether if the fragment contents should be included in the
   news file.


For example:

.. code-block:: toml

    [tool.towncrier]
    [[tool.towncrier.type]]
    directory = "deprecation"
    name = "Deprecations"
    showcontent = true