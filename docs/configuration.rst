Configuration Reference
=======================

``towncrier`` has many knobs and switches you can use, to customize it to your project's needs.
The setup in the :doc:`tutorial` doesn't touch on many, but this document will detail each of these options for you!

For how to perform common customization tasks, see :doc:`customization/index`.

``[tool.towncrier]``
--------------------

All configuration for ``towncrier`` sits inside ``towncrier.toml`` or ``pyproject.toml``, under the ``tool.towncrier`` namespace.
Please see https://toml.io/ for how to write TOML.

A minimal configuration for a Python project looks like this:

.. code-block:: toml

   # pyproject.toml

   [tool.towncrier]
   package = "myproject"

A minimal configuration for a non-Python project looks like this:

.. code-block:: toml

   # towncrier.toml

   [tool.towncrier]
   name = "My Project"

Top level keys
~~~~~~~~~~~~~~

``name``
    The name of your project.

    For Python projects that provide a ``package`` key, if left empty then the name will be automatically determined.

    ``""`` by default.

``version``
    The version of your project.

    Python projects that provide the ``package`` key, if left empty then the version will be automatically determined from the installed package's version metadata or a ``__version__`` variable in the package's module.

    If not provided or able to be determined, the version must be passed explicitly by the command line argument ``--version``.

``directory``
    The directory storing your news fragments.

    For Python projects that provide a ``package`` key, the default is a ``newsfragments`` directory within the package.
    Otherwise the default is a ``newsfragments`` directory relative to either the directory passed as ``--dir`` or (by default) the configuration file.

``filename``
    The filename of your news file.

    ``"NEWS.rst"`` by default.
    Its location is determined the same way as the location of the directory storing the news fragments.

``template``
    Path to the template for generating the news file.

    If the path looks like ``<some.package>:<filename.ext>``, it is interpreted as a template bundled with an installed Python package.

    ``"towncrier:default.rst"`` by default unless ``filename`` ends with ``.md``, in which case the default is ``"towncrier:default.md"``.

``start_string``
    The magic string that ``towncrier`` looks for when considering where the release notes should start.

    ``".. towncrier release notes start\n"`` by default unless ``filename`` ends with ``.md``, in which case the default is ``"<!-- towncrier release notes start -->\n"``.

``title_format``
    A format string for the title of your project.

    The explicit value of ``False`` will disable the title entirely.
    Any other empty value means the template should render the title (the bundled templates use ``<name> <version> (<date>)``).
    Strings should use the following keys to render the title dynamically: ``{name}``, ``{version}``, and ``{project_date}``.

    ``""`` by default.

    Formatted titles are appended a line of ``=`` on the following line (reStructuredText title format) unless the template has an ``.md`` suffix, in which case the title will instead be prefixed with ``#`` (markdown title format).

``issue_format``
    A format string for rendering the issue/ticket number in newsfiles.

    If none, the issues are rendered as ``#<issue>`` if for issues that are integers, or just ``<issue>`` otherwise.
    Use the ``{issue}`` key in your string render the issue number, for example Markdown projects may want to use ``"[{issue}]: https://<your bug tracker>/{issue}"``.

    ``None`` by default.

``underlines``
    The characters used for underlining headers.

    Not used in the bundled Markdown template.

    ``["=", "-", "~"]`` by default.

``wrap``
    Boolean value indicating whether to wrap news fragments to a line length of 79.

    ``false`` by default.

``all_bullets``
    Boolean value indicating whether the template uses bullets for each news fragment.

    ``true`` by default.

``single_file``
    Boolean value indicating whether to write all news fragments to a single file.

    If ``false``, the ``filename`` should use the following keys to render the filenames dynamically:
    ``{name}``, ``{version}``, and ``{project_date}``.

    ``true`` by default.

``orphan_prefix``
    The prefix used for orphaned news fragments.

    ``"+"`` by default.

``create_eof_newline``
    Ensure the content of a news fragment file created with ``towncrier create`` ends with an empty line.

    ``true`` by default.

``create_add_extension``
    Add the ``filename`` option extension to news fragment files created with ``towncrier create`` if an extension is not explicitly provided.

    ``true`` by default.

``ignore``
    A case-insensitive list of filenames in the news fragments directory to ignore.

    ``towncrier check`` will fail if there are any news fragment files that have invalid filenames, except for those in the list. ``towncrier build`` will likewise fail, but only if this list has been configured (set to an empty list if there are no files to ignore).

    Some filenames such as .gitignore, README.rst. README.md, and the template file, are automatically ignored.

    ``None`` by default.

Extra top level keys for Python projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``package``
    The Python package name of your project.

    Allows ``name`` and ``version`` to be automatically determined from the Python package.
    Changes the default ``directory`` to be a ``newsfragments`` directory within this package.

``package_dir``
    The folder your package lives.

    ``"."`` by default, some projects might need to use ``"src"``.


Sections
--------

``towncrier`` supports splitting fragments into multiple sections, each with its own news of fragment types.

Add an array of tables your ``.toml`` configuration file named ``[[tool.towncrier.section]]``.

Each table within this array has the following mandatory keys:


``name``
    The name of the section.

``path``
    The path to the directory containing the news fragments for this section, relative to the configured ``directory``.
    Use ``""`` for the root directory.

For example:

.. code-block:: toml

   [[tool.towncrier.section]]
   name = "Main Platform"
   path = ""

   [[tool.towncrier.section]]
   name = "Secondary"
   path = "secondary"

Section Path Behaviour
~~~~~~~~~~~~~~~~~~~~~~

The path behaviour is slightly different depending on whether ``directory`` is explicitly set.

If ``directory`` is not set, "newsfragments" is added to the end of each path. For example, with the above sections, the paths would be:

:Main Platform:  ./newsfragments
:Secondary:      ./secondary/newsfragments

If ``directory`` *is* set, the section paths are appended to this path. For example, with ``directory = "changes"`` and the above sections, the paths would be:

:Main Platform:  ./changes
:Secondary:      ./changes/secondary


Custom fragment types
---------------------

``towncrier`` has the following default fragment types: ``feature``, ``bugfix``, ``doc``, ``removal``, and ``misc``.

You can use either of the two following method to define custom types instead (you will need to redefine any of the default types you want to use).


Use TOML tables (alphabetical order)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding tables to your ``.toml`` configuration file named ``[tool.towncrier.fragment.<a custom fragment type>]``.

These may include the following optional keys:


``name``
    The description of the fragment type, as it must be included in the news file.

    Defaults to its fragment type, but capitalized.

``showcontent``
    A boolean value indicating whether the fragment contents should be included in the news file.

    ``true`` by default.

    .. note::

        Orphan fragments (those without an issue number) always have their content included.
        If a fragment was created, it means that information is important for end users.

``check``
    A boolean value indicating whether the fragment should be considered by the ``towncrier check`` command.

    ``true`` by default.

For example, if you want your custom fragment types to be ``["feat", "fix", "chore",]`` and you want all of them to use the default configuration except ``"chore"`` you can do it as follows:

.. code-block:: toml

   [tool.towncrier]

   [tool.towncrier.fragment.feat]
   [tool.towncrier.fragment.fix]

   [tool.towncrier.fragment.chore]
   name = "Other Tasks"
   showcontent = false

   [tool.towncrier.fragment.deps]
   name = "Dependency Changes"
   check = false


.. warning::

   Since TOML mappings aren't ordered, types defined using this method are always rendered alphabetically.


Use a TOML Array (defined order)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add an array of tables to your ``.toml`` configuration file named ``[[tool.towncrier.type]]``.

If you use this way to configure custom fragment types, ensure there is no ``tool.towncrier.fragment`` table.

Each table within this array has the following mandatory keys:


``directory``
    The type / category of the fragment.

``name``
    The description of the fragment type, as it must be included
    in the news file.

``showcontent``
    A boolean value indicating whether the fragment contents should be included in the news file.

    ``true`` by default.

    .. note::

        Orphan fragments (those without an issue number) always have their content included.
        If a fragment was created, it means that information is important for end users.

``check``
    A boolean value indicating whether the fragment should be considered by the ``towncrier check`` command.

    ``true`` by default.

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

   [[tool.towncrier.type]]
   directory = "deps"
   name = "Dependency Changes"
   showcontent = true
   check = false
