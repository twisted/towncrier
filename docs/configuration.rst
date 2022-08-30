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
``Towncrier`` allows defining custom fragment types. Custom fragment types
will be used instead ``towncrier`` default ones, they are not combined.

Users can configure each of their own custom fragment types by adding tables to
the pyproject.toml named ``[tool.towncrier.fragment.<a custom fragment type>]``.

These tables may include the following optional keys:

 * ``name``: The description of the fragment type, as it must be included
   in the news file. If omitted, it defaults to  its  fragment type,
   but capitalized.
 * ``showcontent``: Whether if the fragment contents should be included in the
   news file. If omitted, it defaults to ``true``



For example, if you want your custom fragment types to be
``["feat", "fix", "chore",]`` and you want all
of them to use the default configuration except ``"chore"`` you can do it as
follows:


.. code-block:: toml


    [tool.towncrier]


    [tool.towncrier.fragment.feat]
    [tool.towncrier.fragment.fix]

    [tool.towncrier.fragment.chore]
        name = "Other Tasks"
        showcontent = false

DEPRECATED: Defining custom fragment types with an array of toml tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Users can create their own custom fragment types by adding an array of
tables to the pyproject.toml named ``[[tool.towncrier.type]]``.

If still using this way to configure custom fragment types,
please notice that ``fragment_types`` must be empty or not provided.

Each custom type (``[[tool.towncrier.type]]``) has the following
mandatory keys:

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

    [[tool.towncrier.type]]
    directory = "chore"
    name = "Other Tasks"
    showcontent = false
