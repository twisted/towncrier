Tutorial
========

This tutorial assumes you have a Python project with a *reStructuredText* (rst) or *Markdown* (md) news file (also known as changelog) that you wish to use ``towncrier`` on, to generate its news file.
It will cover setting up your project with a basic configuration, which you can then feel free to `customize <customization/index.html>`_.

Install from PyPI::

   python3 -m pip install towncrier


Configuration
-------------

``towncrier`` keeps its config in the `PEP-518 <https://www.python.org/dev/peps/pep-0518/>`_ ``pyproject.toml`` or a ``towncrier.toml`` file.
If the latter exists, it takes precedence.

The most basic configuration is just telling ``towncrier`` where to look for news fragments and what file to generate::

   [tool.towncrier]
   directory = "changes"
   # Where you want your news files to come out, `NEWS.rst` is the default.
   # This can be .rst or .md, towncrier's default template works with both.
   # filename = "NEWS.rst"

Which will look into "./changes" for news fragments and write them into "./NEWS.rst".

If you're working on a Python project, you can also specify a package::

   [tool.towncrier]
   # The name of your Python package
   package = "myproject"
   # The path to your Python package.
   # If your package lives in 'src/myproject/', it must be 'src',
   # but if you don't keep your code in a 'src' dir, remove the
   # config option
   package_dir = "src"

By default, ``towncrier`` will look for news fragments inside your Python package, in a directory named ``newsfragments``.
With this example project, it will look in ``src/myproject/newsfragments/`` for them.

Create this folder::

   $ mkdir src/myproject/newsfragments/
   # This makes sure that Git will never delete the empty folder
   $ echo '!.gitignore' > src/myproject/newsfragments/.gitignore

The ``.gitignore`` will remain and keep Git from not tracking the directory.


Detecting Dates & Versions
--------------------------

``towncrier`` needs to know what version your project is. These are the ways you can provide it (and their order of precedence):

1. Manually pass ``--version=<myversionhere>`` when interacting with ``towncrier``.
2. Set a ``version`` key in your configuration file.
3. For Python projects with a ``package`` key in the configuration file:
   - install the package to use its metadata version information
   - add a ``__version__`` in the top level package that is either a string literal, a tuple, or an `Incremental <https://github.com/twisted/incremental>`_ version

As an example, you can manually specify the version when calling ``towncrier`` on the command line with the ``--version`` flag::

   $ towncrier build --version=1.2.3post4

``towncrier`` will also include the current date (in ``YYYY-MM-DD`` format) when generating news files.
You can change this with the ``--date`` flag::

   $ towncrier build --date=2018-01-01


Creating News Fragments
-----------------------

``towncrier`` news fragments are categorised according to their 'type'.
There are five default types, but you can configure them freely (see `Configuration <configuration.html>`_ for details).

The five default types are:

.. Keep in-sync with DefaultFragmentTypesLoader.

- ``feature``: Signifying a new feature.
- ``bugfix``: Signifying a bug fix.
- ``doc``: Signifying a documentation improvement.
- ``removal``: Signifying a deprecation or removal of public API.
- ``misc``: A ticket has been closed, but it is not of interest to users.

When you create a news fragment, the filename consists of the ticket ID (or some other unique identifier) as well as the 'type'.
``towncrier`` does not care about the fragment's suffix.

You can create those fragments either by hand, or using the ``towncrier create`` command.
Let's create some example news fragments to demonstrate::

   $ echo 'Fixed a thing!' > src/myproject/newsfragments/1234.bugfix
   $ towncrier create --content 'Can also be ``rst`` as well!' 3456.doc.rst
   # You can associate multiple ticket numbers with a news fragment by giving them the same contents.
   $ towncrier create --content 'Can also be ``rst`` as well!' 7890.doc.rst
   $ echo 'The final part is ignored, so set it to whatever you want.' > src/myproject/newsfragments/8765.removal.txt
   $ echo 'misc is special, and does not put the contents of the file in the newsfile.' > src/myproject/newsfragments/1.misc
   $ towncrier create --edit 2.misc.rst  # starts an editor
   $ towncrier create -c "Orphan fragments have no ticket ID." +random.bugfix.rst

For orphan news fragments (those that don't need to be linked to any ticket ID or other identifier), start the file name with ``+``.
The content will still be included in the release notes, at the end of the category corresponding to the file extension::

   $ echo 'Fixed an unreported thing!' > src/myproject/newsfragments/+anything.bugfix

.. The --date is the date of towncrier's first release (15.0.0).

We can then see our news fragments compiled by running ``towncrier`` in draft mode::

   $ towncrier build --draft --name myproject --version 1.0.2 --date 2015-12-27

You should get an output similar to this::

   Loading template...
   Finding news fragments...
   Rendering news fragments...
   Draft only -- nothing has been written.
   What is seen below is what would be written.

   myproject 1.0.2 (2015-12-27)
   ============================

   Bugfixes
   --------

   - Fixed a thing! (#1234)
   - Orphan fragments have no ticket ID.


   Improved Documentation
   ----------------------

   - Can also be ``rst`` as well! (#3456, #7890)


   Deprecations and Removals
   -------------------------

   - The final part is ignored, so set it to whatever you want. (#8765)


   Misc
   ----

   - #1, #2

Note: if you configure a Markdown file (for example, ``filename = "CHANGES.md"``) in your configuration file, the titles will be output in Markdown format instead.

Note: all files (news fragments, the news file, the configuration file, and templates) are encoded and are expected to be encoded as UTF-8.


Producing News Files In Production
----------------------------------

To produce the news file for real, run::

    $ towncrier

This command will remove the news files (with ``git rm``) and append the built news to the filename specified in ``pyproject.toml``, and then stage the news file changes (with ``git add``).
It leaves committing the changes up to the user.

If you wish to have content at the top of the news file (for example, to say where you can find the tickets), put your text above a rST comment that says::

  .. towncrier release notes start

``towncrier`` will then put the version notes after this comment, and leave your existing content that was above it where it is.

Note: if you configure a Markdown file (for example, ``filename = "CHANGES.md"``) in your configuration file, the comment should be ``<!-- towncrier release notes start -->`` instead.


Finale
------

You should now have everything you need to get started with ``towncrier``!
Please see `Customizing <customization/index.html>`_ for some common c tasks, or `Configuration <configuration.html>`_ for the full configuration specification.
