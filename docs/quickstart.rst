Quick Start
===========

This guide assumes you have a Python project that you wish to use ``towncrier`` on, to generate its news files/changelogs.
It will cover setting up your project with a basic configuration, which you can then feel free to `customise <customisation/index.html>`_.

Configuration
-------------

``towncrier`` keeps its config in the `PEP-518 <https://www.python.org/dev/peps/pep-0518/>`_ ``pyproject.toml`` file.

The most basic configuration is annotated below::

    [tool.towncrier]
        # The name of your Python package
        package = "myproject"
        # The path to your Python package.
        # If your package lives in 'src/myproject/', it must be 'src',
        # but if you don't keep your code in a 'src' dir, remove the
        # config option
        package_dir = "src"
        # Where you want your news files to come out. This can be .rst
        # or .md, towncrier's default template works with both.
        filename = "NEWS.rst"

By default, ``towncrier`` will look for news fragments inside your Python package, in a directory named ``newsfragments``.
With this example project, it will look in ``src/myproject/newsfragments/`` for them.

Create this folder::

    $ mkdir src/myproject/newsfragments/
    # This makes sure that Git will never delete the empty folder
    $ echo '!.gitignore' > src/myproject/newsfragments/.gitignore

The ``.gitignore`` will remain and keep Git from not tracking the directory.


Detecting Dates & Versions
--------------------------

``towncrier`` needs to know what version your project is, and there are two ways you can give it:

- For Python 2/3 compatible projects, a ``__version__`` in the top level package.
  This can be either a string literal, a tuple, or an `Incremental <https://github.com/hawkowl/incremental>`_ version.
- Manually passing ``--version=<myversionhere>`` when interacting with ``towncrier``.

As an example, if your package didn't have a ``__version__``, you could manually specify it when calling ``towncrier`` on the command line with the ``--version`` flag::

    $ towncrier --version=1.2.3post4

``towncrier`` will also include the date (in ``YYYY-MM-DD`` format) when generating news files.
You can change this with the ``--date`` flag::

    $ towncrier --date=2018-01-01


Creating News Fragments
-----------------------

``towncrier`` news fragments are categorised according to their 'type'.
There are five default types, but you can configure them freely (see `Configuration <configuration.html>`_ for details).

The five default types are:

- ``feature``: Signifying a new feature.
- ``bugfix``: Signifying a bug fix.
- ``doc``: Signifying a documentation improvement.
- ``removal``: Signifying a deprecation or removal of public API.
- ``misc``: A ticket has been closed, but it is not of interest to users.

When you create a news fragment, the filename consists of the ticket ID (or some other unique identifier) as well as the 'type'.
We can create some example news files to demonstrate::

    $ echo 'Fixed a thing!' > src/myproject/newsfragments/1234.bugfix
    $ echo 'Can also be `rst` as well!' > src/myproject/newsfragments/3456.doc.rst
    $ echo 'The final part is ignored, so set it to whatever you want.' > src/myproject/newsfragments/8765.removal.txt
    $ echo 'misc is special, and does not put the contents of the file in the newsfile.' > src/myproject/newsfragments/1.misc

If the news fragment doesn't need to be linked to any ticket ID or other identifier, start the file name with ``+``::

    $ echo 'Fixed an unreported thing!' > src/myproject/newsfragments/+anything.bugfix

We can then see our news fragments compiled by running ``towncrier`` in draft mode::

    $ towncrier --draft

You should get an output similar to this::

    $ towncrier --draft
    Loading template...
    Finding news fragments...
    Rendering news fragments...
    Draft only -- nothing has been written.
    What is seen below is what would be written.

    myproject 1.0.2 (2017-08-21)
    ============================


    Bugfixes
    --------

    - Fixed an unreported thing!
    - Fixed a thing! (#1234)


    Improved Documentation
    ----------------------

    - Can also be `rst` as well! (#3456)


    Deprecations and Removals
    -------------------------

    - The final part is ignored, so set it to whatever you want. (#8765)


    Misc
    ----

    - #1


Producing News Files In Production
----------------------------------

To produce the news file for real, run::

    $ towncrier

This command will remove the news files (with ``git rm``) and append the built news to the filename specified in ``pyproject.toml``, and then stage the news file changes (with ``git add``).
It leaves committing the changes up to the user.


Finale
------

You should now have everything you need to get started with ``towncrier``!
Please see `Customising <customisation/index.html>`_ for some common customisation tasks, or `Configuration <configuration.html>`_ for the full configuration specification.
