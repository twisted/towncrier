Hear ye, hear ye, says the ``towncrier``
========================================

.. image:: https://img.shields.io/badge/Docs-Read%20The%20Docs-black
   :alt: Documentation
   :target: https://towncrier.readthedocs.io/

.. image:: https://img.shields.io/badge/license-MIT-C06524
   :alt: License: MIT
   :target: https://github.com/twisted/towncrier/blob/trunk/LICENSE

.. image:: https://img.shields.io/pypi/v/towncrier
   :alt: PyPI release
   :target: https://pypi.org/project/towncrier/

``towncrier`` is a utility to produce useful, summarized news files (also known as changelogs) for your project.

Rather than reading the Git history, or having one single file which developers all write to and produce merge conflicts, ``towncrier`` reads "news fragments" which contain information useful to **end users**.

Used by `Twisted <https://github.com/twisted/twisted>`_, `pytest <https://github.com/pytest-dev/pytest/>`_, `pip <https://github.com/pypa/pip/>`_, `BuildBot <https://github.com/buildbot/buildbot>`_, and `attrs <https://github.com/python-attrs/attrs>`_, among others.

While the command line tool ``towncrier`` works on Python 3.7+ only, as long as you don't use any Python-specific affordances (like auto-detection of the project version), it is usable with **any project type** on **any platform**.


Philosophy
----------

``towncrier`` delivers the news which is convenient to those that hear it, not those that write it.

That is, by duplicating what has changed from the "developer log" (which may contain complex information about the original issue, how it was fixed, who authored the fix, and who reviewed the fix) into a "news fragment" (a small file containing just enough information to be useful to end users), ``towncrier`` can produce a digest of the changes which is valuable to those who may wish to use the software.
These fragments are also commonly called "topfiles" or "newsfiles".

``towncrier`` works best in a development system where all merges involve closing a ticket.

To get started, check out our `tutorial <https://towncrier.readthedocs.io/en/latest/tutorial.html>`_!

.. links

Project Links
-------------

- **PyPI**: https://pypi.org/project/towncrier/
- **Documentation**: https://towncrier.readthedocs.io/
- **News**: https://github.com/twisted/towncrier/blob/trunk/NEWS.rst
- **License**: `MIT <https://github.com/twisted/towncrier/blob/trunk/LICENSE>`_
