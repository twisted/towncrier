``towncrier`` issues are filed on `GitHub <https://github.com/hawkowl/towncrier/issues>`_, and each ticket number here corresponds to a closed GitHub issue.

.. towncrier release notes start

towncrier 16.12.0
==========

Bugfixes
--------

- Towncrier will now import the local version of the package and not the global
  one. (#38)

Features
--------

- Allow configration of the template file, title text and "magic comment" (#35)
- Towncrier now uses pyproject.toml, as defined in PEP-518. (#40)


towncrier 16.1.0 (2016-03-25)
=============================

Features
--------

- Ported to Python 2.7. (#27)
- towncrier now supports non-numerical news fragment names. (#32)

Bugfixes
--------

- towncrier would spew an unhelpful exception if it failed importing
  your project when autodiscovering, now it does not. (#22)
- incremental is now added as a runtime dependency for towncrier.
  (#25)

Misc
----

- #33


towncrier 16.0.0 (2016-01-06)
=============================

Features
--------

- towncrier now automatically puts a date beside the version as it is
  generated, using today's date. For repeatable builds, use the
  ``--date`` switch and provide a date. For no date, use ``--date=``.
  (#11)
- towncrier will now add the version logs after ``.. towncrier release
  notes start``, if it is in the file, allowing you to preserve text
  at the top of the file. (#15)

Improved Documentation
----------------------

- The README now mentions how to manually provide the version number,
  for non-Py3 compatible projects. (#19)


towncrier 15.1.0
================

Features
--------

- towncrier now supports reading ``__version__`` attributes that are
  tuples of numbers (e.g. (15, 4, 0)). (#3)
- towncrier now has support for testing via Tox and each commit is now
  ran on Travis CI. (#6)

Bugfixes
--------

- towncrier now defaults to the current working directory for the
  package_dir settings variable. (#2)


towncrier 15.0.0
================

Features
--------

- Basic functionality has been implemented. This includes configuring
  towncrier to find your project, having a set of preconfigured news
  fragment categories, and assembling a newsfile from them. (#1)
