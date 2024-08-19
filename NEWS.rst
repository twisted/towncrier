Release notes
#############

``towncrier`` issues are filed on `GitHub <https://github.com/twisted/towncrier/issues>`_, and each ticket number here corresponds to a closed GitHub issue.

.. towncrier release notes start

Towncrier 24.8.0rc1 (2024-08-19)
================================

Features
--------

- Add ``.gitkeep`` as an ignored filename. (`#643 <https://github.com/twisted/towncrier/issues/643>`_)
- Config `ignore` option now supports wildcard matching via `fnmatch <https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch>`_. (`#644 <https://github.com/twisted/towncrier/issues/644>`_)
- Add a config for enforcing issue names using regex. (`#649 <https://github.com/twisted/towncrier/issues/649>`_)


Bugfixes
--------

- The template file is now ignored based only on the file name. (`#638 <https://github.com/twisted/towncrier/issues/638>`_)
- Control of the header formatting is once again completely up to the user when they are writing markdown files (fixes a regression introduced in [#610](https://github.com/twisted/towncrier/pull/610)). (`#651 <https://github.com/twisted/towncrier/issues/651>`_)
- Fixed an issue where `issue_template` failed recognizing the issue name of files with a non-category suffix (`.md`) (`#654 <https://github.com/twisted/towncrier/issues/654>`_)
- Fixed a bug where orphan news fragments (e.g. +abc1234.feature) would fail when an `issue_pattern` is configured. Orphan news fragments are now excempt from `issue_pattern` checks. (`#655 <https://github.com/twisted/towncrier/issues/655>`_)


Deprecations and Removals
-------------------------

- Moved towncrier version definition from src/towncrier/_version.py to pyproject.toml

  towncrier.__version__ was removed, after being deprecated in 23.6.0. (`#640 <https://github.com/twisted/towncrier/issues/640>`_)


Misc
----

- `#640 <https://github.com/twisted/towncrier/issues/640>`_, `#657 <https://github.com/twisted/towncrier/issues/657>`_


Towncrier 24.7.1 (2024-07-31)
=============================

No significant changes since the previous release candidate.


Bugfixes
--------

- When the template file is stored in the same directory with the news fragments, it is automatically ignored when checking for valid fragment file names. (`#632 <https://github.com/twisted/towncrier/issues/632>`_)


Misc
----

- `#629 <https://github.com/twisted/towncrier/issues/629>`_, `#630 <https://github.com/twisted/towncrier/issues/630>`_


Towncrier 24.7.0 (2024-07-31)
=============================

No changes since the previous release candidate.


Features
--------

- ``towncrier build`` now handles removing news fragments which are not part of the git repository. For example, uncommitted or unstaged files. (`#357 <https://github.com/twisted/towncrier/issues/357>`_)
- Inferring the version of a Python package now tries to use the metadata of the installed package before importing the package explicitly (which only looks for ``[package].__version__``). (`#432 <https://github.com/twisted/towncrier/issues/432>`_)
- If no filename is given when doing ``towncrier`` create, interactively ask for the issue number and fragment type (and then launch an interactive editor for the fragment content).

  Now by default, when creating a fragment it will be appended with the ``filename`` option's extension (unless an extension is explicitly provided). For example, ``towncrier create 123.feature`` will create ``news/123.feature.rst``. This can be changed in configuration file by setting `add_extension = false`.

  A new line is now added by default to the end of the fragment contents. This can be reverted in the configuration file by setting `add_newline = false`. (`#482 <https://github.com/twisted/towncrier/issues/482>`_)
- The temporary file ``towncrier create`` creates now uses the correct ``.rst`` or ``.md`` extension, which may help your editor with with syntax highlighting. (`#594 <https://github.com/twisted/towncrier/issues/594>`_)
- Running ``towncrier`` will now traverse back up directories looking for the configuration file. (`#601 <https://github.com/twisted/towncrier/issues/601>`_)
- The ``towncrier create`` action now uses sections defined in your config (either interactively, or via the new ``--section`` option). (`#603 <https://github.com/twisted/towncrier/issues/603>`_)
- News fragments are now sorted by issue number even if they have non-digit characters.

  For example::

      - some issue (gh-3, gh-10)
      - another issue (gh-4)
      - yet another issue (gh-11)

  The sorting algorithm groups the issues first by non-text characters and then by number. (`#608 <https://github.com/twisted/towncrier/issues/608>`_)
- The ``title_format`` configuration option now uses a markdown format for markdown templates. (`#610 <https://github.com/twisted/towncrier/issues/610>`_)
- newsfragment categories can now be marked with ``check = false``, causing them to be ignored in ``towncrier check`` (`#617 <https://github.com/twisted/towncrier/issues/617>`_)
- ``towncrier check`` will now fail if any news fragments have invalid filenames.

  Added a new configuration option called ``ignore`` that allows you to specify a list of filenames that should be ignored. If this is set, ``towncrier build`` will also fail if any filenames are invalid, except for those in the list. (`#622 <https://github.com/twisted/towncrier/issues/622>`_)


Bugfixes
--------

- Add explicit encoding to read_text. (`#561 <https://github.com/twisted/towncrier/issues/561>`_)
- The default Markdown template now renders a title containing the release version and date, even when the `name` configuration is left empty. (`#587 <https://github.com/twisted/towncrier/issues/587>`_)
- Orphan news fragments, fragments not associated with an issue, consisting of only digits (e.g. '+12345678.feature') now retain their leading marker character. (`#588 <https://github.com/twisted/towncrier/issues/588>`_)
- Orphan news fragments, fragments not associated with an issue, will now still show in categories that are marked to not show content, since they do not have an issue number to show. (`#612 <https://github.com/twisted/towncrier/issues/612>`_)


Improved Documentation
----------------------

- Clarify version discovery behavior. (`#432 <https://github.com/twisted/towncrier/issues/432>`_, `#602 <https://github.com/twisted/towncrier/issues/602>`_)
- The tutorial now introduces the `filename` option in the appropriate paragraph and mentions its default value. (`#586 <https://github.com/twisted/towncrier/issues/586>`_)
- Add docs to explain how ``towncrier create +.feature.rst`` (orphan fragments) works. (`#589 <https://github.com/twisted/towncrier/issues/589>`_)


Misc
----

- `#491 <https://github.com/twisted/towncrier/issues/491>`_, `#561 <https://github.com/twisted/towncrier/issues/561>`_, `#562 <https://github.com/twisted/towncrier/issues/562>`_, `#568 <https://github.com/twisted/towncrier/issues/568>`_, `#569 <https://github.com/twisted/towncrier/issues/569>`_, `#571 <https://github.com/twisted/towncrier/issues/571>`_, `#574 <https://github.com/twisted/towncrier/issues/574>`_, `#575 <https://github.com/twisted/towncrier/issues/575>`_, `#582 <https://github.com/twisted/towncrier/issues/582>`_, `#591 <https://github.com/twisted/towncrier/issues/591>`_, `#596 <https://github.com/twisted/towncrier/issues/596>`_, `#597 <https://github.com/twisted/towncrier/issues/597>`_, `#625 <https://github.com/twisted/towncrier/issues/625>`_


towncrier 23.11.0 (2023-11-08)
==============================

No significant changes since the previous release candidate.


Bugfixes
--------

- ``build`` now treats a missing fragments directory the same as an empty one, consistent with other operations. (`#538 <https://github.com/twisted/towncrier/issues/538>`_)
- Fragments with filenames like `fix-1.2.3.feature` are now associated with the issue `fix-1.2.3`.
  In previous versions they were incorrectly associated to issue `3`. (`#562 <https://github.com/twisted/towncrier/issues/562>`_)
- Orphan newsfragments containing numeric values are no longer accidentally associated to issues. In previous versions the orphan marker was ignored and the newsfragment was associated to an issue having the last numerical value from the filename. (`#562 <https://github.com/twisted/towncrier/issues/562>`_)


Misc
----

- `#558 <https://github.com/twisted/towncrier/issues/558>`_, `#559 <https://github.com/twisted/towncrier/issues/559>`_


towncrier 23.10.0 (2023-10-24)
==============================

No significant changes since the previous release candidate.


Features
--------

- Python 3.12 is now officially supported. (`#541 <https://github.com/twisted/towncrier/issues/541>`_)
- Initial support was added for monorepo-style setup.
  One project with multiple independent news files stored in separate sub-directories, that share the same towncrier config. (`#548 <https://github.com/twisted/towncrier/issues/548>`_)
- Two newlines are no longer always added between the current release notes and the previous content.
  The newlines are now defined only inside the template.

  **Important! If you're using a custom template and want to keep the same whitespace between releases, you may have to modify your template.** (`#552 <https://github.com/twisted/towncrier/issues/552>`_)


Bugfixes
--------

- Towncrier now vendors the click-default-group package that prevented installations on modern Pips. (`#540 <https://github.com/twisted/towncrier/issues/540>`_)


Improved Documentation
----------------------

- The markdown docs now use the default markdown template rather than a simpler custom one. (`#545 <https://github.com/twisted/towncrier/issues/545>`_)
- Cleanup a duplicate backtick in the tutorial. (`#551 <https://github.com/twisted/towncrier/issues/551>`_)


Deprecations and Removals
-------------------------

- The support for Python 3.7 has been dropped. (`#521 <https://github.com/twisted/towncrier/issues/521>`_)


Misc
----

- `#481 <https://github.com/twisted/towncrier/issues/481>`_, `#520 <https://github.com/twisted/towncrier/issues/520>`_, `#522 <https://github.com/twisted/towncrier/issues/522>`_, `#523 <https://github.com/twisted/towncrier/issues/523>`_, `#529 <https://github.com/twisted/towncrier/issues/529>`_, `#536 <https://github.com/twisted/towncrier/issues/536>`_


towncrier 23.6.0 (2023-06-06)
=============================

This is the last release to support Python 3.7.


Features
--------

- Make ``towncrier create`` use the fragment counter rather than failing
  on existing fragment names.

  For example, if there is an existing fragment named ``123.feature``,
  then ``towncrier create 123.feature`` will now create a fragment
  named ``123.feature.1``. (`#475 <https://github.com/twisted/towncrier/issues/475>`_)
- Provide a default Markdown template if the configured filename ends with ``.md``.

  The Markdown template uses the same rendered format as the default *reStructuredText* template, but with a Markdown syntax. (`#483 <https://github.com/twisted/towncrier/issues/483>`_)
- Towncrier no longer depends on setuptools & uses importlib.resources (or its backport) instead. (`#496 <https://github.com/twisted/towncrier/issues/496>`_)
- Added pre-commit hooks for checking and updating news in projects using pre-commit. (`#498 <https://github.com/twisted/towncrier/issues/498>`_)
- Calling ``towncrier check`` without an existing configuration, will just show only an error message.

  In previous versions, a traceback was generated instead of the error message. (`#501 <https://github.com/twisted/towncrier/issues/501>`_)


Bugfixes
--------

- Fix creating fragment in a section not adding random characters.

  For example, ``towncrier create some_section/+.feature`` should end up as a fragment named something like ``news/some_section/+a4e22da1.feature``. (`#468 <https://github.com/twisted/towncrier/issues/468>`_)
- Fix the ReadTheDocs build for ``towncrier`` which was broken due to the python version in use being 3.8. Upgrade to 3.11. (`#509 <https://github.com/twisted/towncrier/issues/509>`_)


Improved Documentation
----------------------

- Moved man page to correct section (`#470 <https://github.com/twisted/towncrier/issues/470>`_)
- Update link to Quick Start in configuration.html to point to Tutorial instead. (`#504 <https://github.com/twisted/towncrier/issues/504>`_)
- Add a note about the build command's ``--version`` requiring the command to be explicitly passed. (`#511 <https://github.com/twisted/towncrier/issues/511>`_)
- Fix typos in the Pre-Commit docs. (`#512 <https://github.com/twisted/towncrier/issues/512>`_)


Misc
----

- `#459 <https://github.com/twisted/towncrier/issues/459>`_, `#462 <https://github.com/twisted/towncrier/issues/462>`_, `#472 <https://github.com/twisted/towncrier/issues/472>`_, `#485 <https://github.com/twisted/towncrier/issues/485>`_, `#486 <https://github.com/twisted/towncrier/issues/486>`_, `#487 <https://github.com/twisted/towncrier/issues/487>`_, `#488 <https://github.com/twisted/towncrier/issues/488>`_, `#495 <https://github.com/twisted/towncrier/issues/495>`_, `#497 <https://github.com/twisted/towncrier/issues/497>`_, `#507 <https://github.com/twisted/towncrier/issues/507>`_, `#1117 <https://github.com/twisted/towncrier/issues/1117>`_, `#513 <https://github.com/twisted/towncrier/issues/513>`_


towncrier 22.12.0 (2022-12-21)
==============================

No changes since the previous release candidate.


towncrier 22.12.0rc1 (2022-12-20)
=================================

Features
--------

- Added ``--keep`` option to the ``build`` command that allows generating a newsfile, but keeps the newsfragments in place.
  This option can not be used together with ``--yes``. (`#129 <https://github.com/twisted/towncrier/issues/129>`_)
- Python 3.11 is now officially supported. (`#427 <https://github.com/twisted/towncrier/issues/427>`_)
- You can now create fragments that are not associated with issues. Start the name of the fragment with ``+`` (e.g. ``+anything.feature``).
  The content of these orphan news fragments will be included in the release notes, at the end of the category corresponding to the file extension.

  To help quickly create a unique orphan news fragment, ``towncrier create +.feature`` will append a random string to the base name of the file, to avoid name collisions. (`#428 <https://github.com/twisted/towncrier/issues/428>`_)


Improved Documentation
----------------------

- Improved contribution documentation. (`#415 <https://github.com/twisted/towncrier/issues/415>`_)
- Correct a typo in the readme that incorrectly documented custom fragments in a format that does not work. (`#424 <https://github.com/twisted/towncrier/issues/424>`_)
- The documentation has been restructured and (hopefully) improved. (`#435 <https://github.com/twisted/towncrier/issues/435>`_)
- Added a Markdown-based how-to guide. (`#436 <https://github.com/twisted/towncrier/issues/436>`_)
- Defining custom fragments using a TOML array is not deprecated anymore. (`#438 <https://github.com/twisted/towncrier/issues/438>`_)


Deprecations and Removals
-------------------------

- Default branch for `towncrier check` is now "origin/main" instead of "origin/master".
  If "origin/main" does not exist, fallback to "origin/master" with a deprecation warning. (`#400 <https://github.com/twisted/towncrier/issues/400>`_)


Misc
----

- `#406 <https://github.com/twisted/towncrier/issues/406>`_, `#408 <https://github.com/twisted/towncrier/issues/408>`_, `#411 <https://github.com/twisted/towncrier/issues/411>`_, `#412 <https://github.com/twisted/towncrier/issues/412>`_, `#413 <https://github.com/twisted/towncrier/issues/413>`_, `#414 <https://github.com/twisted/towncrier/issues/414>`_, `#416 <https://github.com/twisted/towncrier/issues/416>`_, `#418 <https://github.com/twisted/towncrier/issues/418>`_, `#419 <https://github.com/twisted/towncrier/issues/419>`_, `#421 <https://github.com/twisted/towncrier/issues/421>`_, `#429 <https://github.com/twisted/towncrier/issues/429>`_, `#430 <https://github.com/twisted/towncrier/issues/430>`_, `#431 <https://github.com/twisted/towncrier/issues/431>`_, `#434 <https://github.com/twisted/towncrier/issues/434>`_, `#446 <https://github.com/twisted/towncrier/issues/446>`_, `#447 <https://github.com/twisted/towncrier/issues/447>`_


towncrier 22.8.0 (2022-08-29)
=============================

No significant changes since the previous release candidate.


towncrier 22.8.0.rc1 (2022-08-28)
=================================

Features
--------

- Make the check subcommand succeed for branches that change the news file

  This should enable the ``check`` subcommand to be used as a CI lint step and
  not fail when a pull request only modifies the configured news file (i.e. when
  the news file is being assembled for the next release). (`#337 <https://github.com/twisted/towncrier/issues/337>`_)
- Added support to tables in toml settings, which provides a more intuitive
  way to configure custom types. (`#369 <https://github.com/twisted/towncrier/issues/369>`_)
- The `towncrier create` command line now has a new `-m TEXT` argument that is used to define the content of the newly created fragment. (`#374 <https://github.com/twisted/towncrier/issues/374>`_)


Bugfixes
--------

- The extra newline between the title and rendered content when using ``--draft`` is no longer inserted. (`#105 <https://github.com/twisted/towncrier/issues/105>`_)
- The detection of duplicate release notes was fixed and recording changes of same version is no longer triggered.

  Support for having the release notes for each version in a separate file is working again. This is a regression introduced in VERSION 19.9.0rc1. (`#391 <https://github.com/twisted/towncrier/issues/391>`_)


Improved Documentation
----------------------

- Improve ``CONTRIBUTING.rst`` and add PR template. (`#342 <https://github.com/twisted/towncrier/issues/342>`_)
- Move docs too the main branch and document custom fragment types. (`#367 <https://github.com/twisted/towncrier/issues/367>`_)
- The CLI help messages were updated to contain more information. (`#384 <https://github.com/twisted/towncrier/issues/384>`_)


Deprecations and Removals
-------------------------

- Support for all Python versions older than 3.7 has been dropped. (`#378 <https://github.com/twisted/towncrier/issues/378>`_)


Misc
----

- `#292 <https://github.com/twisted/towncrier/issues/292>`_, `#330 <https://github.com/twisted/towncrier/issues/330>`_, `#366 <https://github.com/twisted/towncrier/issues/366>`_, `#376 <https://github.com/twisted/towncrier/issues/376>`_, `#377 <https://github.com/twisted/towncrier/issues/377>`_, `#380 <https://github.com/twisted/towncrier/issues/380>`_, `#381 <https://github.com/twisted/towncrier/issues/381>`_, `#382 <https://github.com/twisted/towncrier/issues/382>`_, `#383 <https://github.com/twisted/towncrier/issues/383>`_, `#393 <https://github.com/twisted/towncrier/issues/393>`_, `#399 <https://github.com/twisted/towncrier/issues/399>`_, `#402 <https://github.com/twisted/towncrier/issues/402>`_


towncrier 21.9.0 (2022-02-04)
=============================

Features
--------

- towncrier --version` was added to the command line interface to show the product version. (`#339 <https://github.com/twisted/towncrier/issues/339>`_)
- Support Toml v1 syntax with tomli on Python 3.6+ (`#354 <https://github.com/twisted/towncrier/issues/354>`_)


Bugfixes
--------

- Stop writing title twice when ``title_format`` is specified. (`#346 <https://github.com/twisted/towncrier/issues/346>`_)
- Disable universal newlines when reading TOML (`#359 <https://github.com/twisted/towncrier/issues/359>`_)


Misc
----

- `#332 <https://github.com/twisted/towncrier/issues/332>`_, `#333 <https://github.com/twisted/towncrier/issues/333>`_, `#334 <https://github.com/twisted/towncrier/issues/334>`_, `#338 <https://github.com/twisted/towncrier/issues/338>`_


towncrier 21.3.0 (2021-04-02)
=============================

No significant changes since the previous release candidate.


towncrier 21.3.0.rc1 (2021-03-21)
=================================

Features
--------

- Issue number from file names will be stripped down to avoid issue links such as ``#007``. (`#126 <https://github.com/twisted/towncrier/issues/126>`_)
- Allow definition of the project ``version`` and ``name`` in the configuration file.
  This allows use of towncrier seamlessly with non-Python projects. (`#165 <https://github.com/twisted/towncrier/issues/165>`_)
- Improve news fragment file name parsing to allow using file names like
  ``123.feature.1.ext`` which are convenient when one wants to use an appropriate
  extension (e.g. ``rst``, ``md``) to enable syntax highlighting. (`#173 <https://github.com/twisted/towncrier/issues/173>`_)
- The new ``--edit`` option of the ``create`` subcommand launches an editor for entering the contents of the newsfragment. (`#275 <https://github.com/twisted/towncrier/issues/275>`_)
- CPython 3.8 and 3.9 are now part of our automated test matrix and are officially supported. (`#291 <https://github.com/twisted/towncrier/issues/291>`_)
- When searching for the project, first check for an existing importable instance.
  This helps if the version is only available in the installed version and not the source. (`#297 <https://github.com/twisted/towncrier/issues/297>`_)
- Support building with PEP 517. (`#314 <https://github.com/twisted/towncrier/issues/314>`_)


Bugfixes
--------

- Configuration errors found during command line execution now trigger a message to stderr and no longer show a traceback. (`#84 <https://github.com/twisted/towncrier/issues/84>`_)
- A configuration error is triggered when the newsfragment files couldn't be discovered. (`#85 <https://github.com/twisted/towncrier/issues/85>`_)
- Invoking towncrier as `python -m towncrier` works. (`#163 <https://github.com/twisted/towncrier/issues/163>`_)
- ``check`` subcommand defaults to UTF-8 encoding when ``sys.stdout.encoding`` is ``None``.
  This happens, for example, with Python 2 on GitHub Actions or when the output is piped. (`#175 <https://github.com/twisted/towncrier/issues/175>`_)
- Specifying ``title_format`` disables default top line creation to avoid duplication. (`#180 <https://github.com/twisted/towncrier/issues/180>`_)


Improved Documentation
----------------------

- The README now mentions the possibility to name the configuration file
  ``towncrier.toml`` (in addition to ``pyproject.toml``). (`#172 <https://github.com/twisted/towncrier/issues/172>`_)
- ``start_line`` corrected to ``start_string`` in the readme to match the long standing implementation. (`#277 <https://github.com/twisted/towncrier/issues/277>`_)


towncrier 19.9.0 (2021-03-20)
=============================

No significant changes.


towncrier 19.9.0rc1 (2019-09-16)
================================

Features
--------

- Add ``create`` subcommand, which can be used to quickly create a news
  fragment command in the location defined by config. (`#4 <https://github.com/twisted/towncrier/issues/4>`_)
- Add support for subcommands, meaning the functionality of the ``towncrier``
  executable is now replaced by the ``build`` subcommand::

      $ towncrier build --draft

  A new ``check`` subcommand is exposed. This is an alternative to calling the
  ``towncrier.check`` module manually::

      $ towncrier check

  Calling ``towncrier`` without a subcommand will result in a call to the
  ``build`` subcommand to ensure backwards compatibility. This may be removed in a
  future release. (`#144 <https://github.com/twisted/towncrier/issues/144>`_)
- Towncrier's templating now allows configuration of the version header. *CUSTOM TEMPLATE USERS PLEASE NOTE: You will need to add the version header information to your template!* (`#147 <https://github.com/twisted/towncrier/issues/147>`_)
- towncrier now accepts the --config argument to specify a custom configuration file (`#157 <https://github.com/twisted/towncrier/issues/157>`_)
- There is now the option for ``all_bullets = false`` in the configuration.
  Setting ``all_bullets`` to false means that news fragments have to include
  the bullet point if they should be rendered as enumerations, otherwise
  they are rendered directly (this means fragments can include a header.).
  It is necessary to set this option to avoid (incorrect) automatic indentation
  of multiline fragments that do not include bullet points.
  The ``single-file-no-bullets.rst`` template gives an example of
  using these options. (`#158 <https://github.com/twisted/towncrier/issues/158>`_)
- The ``single_file`` option can now be added to the configuration file. When set to ``true``, the filename key can now be formattable with the ``name``, ``version``, and ``project_date`` format variables. This allows subsequent versions to be written out to new files instead of appended to an existing one. (`#161 <https://github.com/twisted/towncrier/issues/161>`_)
- You can now specify Towncrier-bundled templates in your configuration file. Available templates are `default`, `hr-between-versions` (as used in attrs), and `single-file-no-bullets`. (`#162 <https://github.com/twisted/towncrier/issues/162>`_)


Bugfixes
--------

- Accept newsfragment filenames with multiple dots, like `fix-1.2.3.bugfix`. (`#142 <https://github.com/twisted/towncrier/issues/142>`_)


Deprecations and Removals
-------------------------

- The `--pyproject` option for `towncrier check` is now replaced with `--config`, for consistency with other commands. (`#162 <https://github.com/twisted/towncrier/issues/162>`_)


towncrier 19.2.0 (2019-02-15)
=============================

Features
--------

- Add support for multiple fragements per issue/type pair. This extends the
  naming pattern of the fragments to `issuenumber.type(.counter)` where counter
  is an optional integer. (`#119 <https://github.com/twisted/towncrier/issues/119>`_)
- Python 2.7 is now supported. (`#121 <https://github.com/twisted/towncrier/issues/121>`_)
- `python -m towncrier.check` now accepts an option to give the configuration file location. (`#123 <https://github.com/twisted/towncrier/issues/123>`_)
- towncrier.check now reports git output when it encounters a git failure. (`#124 <https://github.com/twisted/towncrier/issues/124>`_)


towncrier 18.6.0 (2018-07-05)
=============================

Features
--------

- ``python -m towncrier.check``, which will check a Git branch for the presence of added newsfiles, to be used in a CI system. (`#75 <https://github.com/twisted/towncrier/issues/75>`_)
- wrap is now an optional configuration option (which is False by default) which controls line wrapping of news files. Towncrier will now also not attempt to normalise (wiping newlines) from the input, but will strip leading and ending whitespace. (`#80 <https://github.com/twisted/towncrier/issues/80>`_)
- Towncrier can now be invoked by ``python -m towncrier``. (`#115 <https://github.com/twisted/towncrier/issues/115>`_)


Deprecations and Removals
-------------------------

- Towncrier now supports Python 3.5+ as a script runtime. Python 2.7 will not function. (`#80 <https://github.com/twisted/towncrier/issues/80>`_)


towncrier 18.5.0 (2018-05-16)
=============================

Features
--------

- Python 3.3 is no longer supported. (`#103
  <https://github.com/twisted/towncrier/issues/103>`_)
- Made ``package`` optional. When the version is passed on the command line,
  and the ``title_format`` does not use the package name, and it is not used
  for the path to the news fragments, then no package name is needed, so we
  should not enforce it. (`#111
  <https://github.com/twisted/towncrier/issues/111>`_)


Bugfixes
--------

- When cleaning up old newsfragments, if a newsfragment is named
  "123.feature.rst", then remove that file instead of trying to remove the
  non-existent "123.feature". (`#99
  <https://github.com/twisted/towncrier/issues/99>`_)
- If there are two newsfragments with the same name (example: "123.bugfix.rst"
  and "123.bugfix.rst~"), then raise an error instead of silently picking one
  at random. (`#101 <https://github.com/twisted/towncrier/issues/101>`_)


towncrier 17.8.0 (2017-08-19)
=============================

Features
--------

- Added new option ``issue_format``. For example, this can be used to make
  issue text in the NEWS file be formatted as ReST links to the issue tracker.
  (`#52 <https://github.com/twisted/towncrier/issues/52>`_)
- Add ``--yes`` option to run non-interactively. (`#56
  <https://github.com/twisted/towncrier/issues/56>`_)
- You can now name newsfragments like 123.feature.rst, or 123.feature.txt, or
  123.feature.whatever.you.want, and towncrier will ignore the extension. (`#62
  <https://github.com/twisted/towncrier/issues/62>`_)
- New option in ``pyproject.toml``: ``underlines = ["=", "-", "~"]`` to specify
  the ReST underline hierarchy in towncrier's generated text. (`#63
  <https://github.com/twisted/towncrier/issues/63>`_)
- Instead of sorting sections/types alphabetically (e.g. "bugfix" before
  "feature" because "b" < "f"), sections/types will now have the same order in
  the output as they have in your config file. (`#70
  <https://github.com/twisted/towncrier/issues/70>`_)


Bugfixes
--------

- When rewrapping text, don't break words or at hyphens -- they might be inside
  a URL (`#68 <https://github.com/twisted/towncrier/issues/68>`_)


Deprecations and Removals
-------------------------

- `towncrier.ini` config file support has been removed in preference to
  `pyproject.toml` configuration. (`#71
  <https://github.com/twisted/towncrier/issues/71>`_)


towncrier 17.4.0 (2017-04-15)
=============================

Misc
----

- #46


towncrier 17.1.0
================

Bugfixes
--------

- fix --date being ignored (#43)


towncrier 16.12.0
=================

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
