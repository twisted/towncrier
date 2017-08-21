Hear ye, hear ye, says the ``towncrier``
========================================

.. image:: https://travis-ci.org/hawkowl/towncrier.svg?branch=master
    :target: https://travis-ci.org/hawkowl/towncrier

.. image:: https://codecov.io/github/hawkowl/towncrier/coverage.svg?branch=master
    :target: https://codecov.io/github/hawkowl/towncrier?branch=master

``towncrier`` is a utility to produce useful, summarised news files for your project.
Rather than reading the Git history or having one single file which developers all write to, ``towncrier`` reads "news fragments" which contain information `useful to end users`.
This allows you to put developer-focused content in your Git commits, and user-focused content in your changelogs, without ever having to worry about a ``CHANGELOG`` merge conflict again!

``towncrier`` was originally designed for Python projects, but can be used by projects written in any language, only requiring Python to collate the newsfiles during the release process.
It is not required to create news fragments.


Philosophy
----------

``towncrier`` delivers the news which is convenient to those that hear it, not those that write it.

That is, by duplicating what has changed from the "developer log" (which may contain complex information about the original issue, how it was fixed, who authored the fix, and who reviewed the fix) into a "news fragment" (a small file containing just enough information to be useful to end users), ``towncrier`` can produce a digest of the changes which is valuable to those who may wish to use the software.
These fragments are also commonly called "topfiles" or "newsfiles" in Twisted parlance.

``towncrier`` works best in a development system where all merges involve closing a ticket.


Installation
------------

Install from PyPI::

    $ python3 -m pip install towncrier
    # OR:
    $ python2 -m pip install towncrier


Usage
-----

Once your project is `set up <https://towncrier.readthedocs.io/en/latest/quickstart.html>`_, the ``towncrier`` command will allow you to generate your newsfiles::

    # Generates and writes your changelog
    $ towncrier

    # Gives you a draft of what would be written, without making changes
    $ towncrier --draft


Documentation
-------------

The `full documentation <https://towncrier.readthedocs.io/>`_ lives on Read The Docs.
