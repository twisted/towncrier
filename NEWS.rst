``towncrier`` issues are filed on `GitHub <https://github.com/hawkowl/towncrier/issues>`_, and each ticket number here corresponds to a closed GitHub issue.

.. towncrier release notes start

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
