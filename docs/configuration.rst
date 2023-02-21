Configuration Reference
=======================

``towncrier`` has many knobs and switches you can use, to customize it to your project's needs.
The setup in the `Quick Start <quickstart.html>`_ doesn't touch on many, but this document will detail each of these options for you!

For how to perform common customization tasks, see `Customization <customization/index.html>`_.

``[tool.towncrier]``
--------------------

All configuration for ``towncrier`` sits inside ``pyproject.toml``, under the ``tool.towncrier`` namespace.
Please see https://toml.io/ for how to write TOML.


Top level keys
~~~~~~~~~~~~~~

- ``directory`` -- If you are not storing your news fragments in your Python package, or aren't using Python, this is the path to where your newsfragments will be put.
- ``filename`` -- The filename of your news file.
  ``NEWS.rst`` by default.
- ``package`` -- The package name of your project.
  (Python projects only)
- ``package_dir`` -- The folder your package lives. ``./`` by default, some projects might need to use ``src``.
  (Python projects only)
- ``template`` -- Path to an alternate template for generating the news file, if you have one.
- ``start_string`` -- The magic string that ``towncrier`` looks for when considering where the release notes should start.
  ``.. towncrier release notes start`` by default.
- ``title_format`` -- A format string for the title of your project.
  ``{name} {version} ({project_date})`` by default.
- ``issue_format`` -- A format string for rendering the issue/ticket number in newsfiles.
  ``#{issue}`` by default.
- ``underlines`` -- The characters used for underlining headers.
  ``["=", "-", "~"]`` by default.


Custom fragment types
---------------------
``towncrier`` allows defining custom fragment types.
Custom fragment types will be used instead ``towncrier`` default ones, they are not combined.

There are two ways to add custom fragment types.


Defining Custom Fragment Types With a TOML Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Users can configure each of their own custom fragment types by adding tables to
the pyproject.toml named ``[tool.towncrier.fragment.<a custom fragment type>]``.

These tables may include the following optional keys:

 * ``name``: The description of the fragment type, as it must be included in the news file.
   If omitted, it defaults to  its  fragment type, but capitalized.
 * ``showcontent``: Whether if the fragment contents should be included in the news file. If omitted, it defaults to ``true``

For example, if you want your custom fragment types to be ``["feat", "fix", "chore",]`` and you want all of them to use the default configuration except ``"chore"`` you can do it as follows:

.. code-block:: toml

   [tool.towncrier]

   [tool.towncrier.fragment.feat]
   [tool.towncrier.fragment.fix]

   [tool.towncrier.fragment.chore]
   name = "Other Tasks"
   showcontent = false


.. warning::

   Since TOML mappings aren't ordered, the sections are always rendered alphabetically.


Defining Custom Fragment Types With an Array of TOML Tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Users can create their own custom fragment types by adding an array of
tables to the pyproject.toml named ``[[tool.towncrier.type]]``.

If you use this way to configure custom fragment types, please note that ``fragment_types`` must be empty or not provided.

Each custom type (``[[tool.towncrier.type]]``) has the following
mandatory keys:

* ``directory``: The type / category of the fragment.
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


All Options
-----------

``towncrier`` has the following global options, which can be specified in the toml file:

.. code-block:: toml

   [tool.towncrier]
   package = ""
   package_dir = "."
   single_file = true  # if false, filename is formatted like `title_format`.
   filename = "NEWS.rst"
   directory = "directory/of/news/fragments"
   version = "1.2.3"  # project version if maintained separately
   name = "arbitrary project name"
   template = "path/to/template.rst"
   start_string = "Text used to detect where to add the generated content in the middle of a file. Generated content added after this text. Newline auto added."
   title_format = "{name} {version} ({project_date})"  # or false if template includes title
   issue_format = "format string for {issue} (issue is the first part of fragment name)"
   underlines = "=-~"
   wrap = false  # Wrap text to 79 characters
   all_bullets = true  # make all fragments bullet points
   orphan_prefix = "+"   # Prefix for orphan news fragment files, set to "" to disable.
   create_eof_newline = true  # Ensure the content of a news fragment file created with ``towncrier create`` ends with an empty line.
   create_add_extension = true  # Add the ``filename`` option extension to news fragment files created with ``towncrier create`` (if extension not explicitly provided).

If ``single_file`` is set to ``true`` or unspecified, all changes will be written to a single fixed newsfile, whose name is literally fixed as the ``filename`` option.
In each run of ``towncrier build``, content of new changes will append at the top of old content, and after ``start_string`` if the ``start_string`` already appears in the newsfile.
If the corresponding ``top_line``, which is formatted as the option 'title_format', already exists in newsfile, ``ValueError`` will be raised to remind you "already produced newsfiles for this version".

If ``single_file`` is set to ``false`` instead, each versioned ``towncrier build`` will generate a separate newsfile, whose name is formatted as the pattern given by option ``filename``.
For example, if ``filename="{version}-notes.rst"``, then the release note with version "7.8.9" will be written to the file "7.8.9-notes.rst".
If the newsfile already exists, its content will be overwritten with new release note, without throwing a ``ValueError`` warning.

If ``title_format`` is unspecified or an empty string, the default format will be used.
If set to ``false``, no title will be created.
This can be useful if the specified template creates the title itself.
