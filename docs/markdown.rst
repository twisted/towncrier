How to Keep a Changelog in Markdown
===================================

`Keep a Changelog <https://keepachangelog.com/>`_ is a standardized way to format a news file in `Markdown <https://en.wikipedia.org/wiki/Markdown>`_.

This guide shows you how to configure ``towncrier`` for keeping a Markdown-based news file of a project without using any Python-specific features.
Everything used here can be used with any other language or platform.

This guide makes the following assumptions:

- The project lives at https://github.com/twisted/my-project/.
- The news file name is ``CHANGELOG.md``.
- You store the news fragments in the ``changelog.d`` directory at the root of the project.

Put the following into your ``pyproject.toml`` or ``towncrier.toml``:

.. code-block:: toml

   [tool.towncrier]
   directory = "changelog.d"
   filename = "CHANGELOG.md"
   start_string = "<!-- towncrier release notes start -->\n"
   underlines = ["", "", ""]
   template = "changelog.d/changelog_template.jinja"
   title_format = "## [{version}](https://github.com/twisted/my-project/tree/{version}) - {project_date}"
   issue_format = "[#{issue}](https://github.com/twisted/my-project/issues/{issue})"

   [[tool.towncrier.type]]
   directory = "security"
   name = "Security"
   showcontent = true

   [[tool.towncrier.type]]
   directory = "removed"
   name = "Removed"
   showcontent = true

   [[tool.towncrier.type]]
   directory = "deprecated"
   name = "Deprecated"
   showcontent = true

   [[tool.towncrier.type]]
   directory = "added"
   name = "Added"
   showcontent = true

   [[tool.towncrier.type]]
   directory = "changed"
   name = "Changed"
   showcontent = true

   [[tool.towncrier.type]]
   directory = "fixed"
   name = "Fixed"
   showcontent = true



Next create the news fragment directory and the news file template:

.. code-block:: console

   $ mkdir changelog.d

And put the following into ``changelog.d/changelog_template.jinja``:

.. code-block:: jinja

   {% if sections[""] %}
   {% for category, val in definitions.items() if category in sections[""] %}

   ### {{ definitions[category]['name'] }}

   {% for text, values in sections[""][category].items() %}
   - {{ text }} {{ values|join(', ') }}
   {% endfor %}

   {% endfor %}
   {% else %}
   No significant changes.


   {% endif %}


Next, create the news file with an explanatory header::

   $ cat >CHANGELOG.md <<EOF
   # Changelog

   All notable changes to this project will be documented in this file.

   The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

   This project uses [*towncrier*](https://towncrier.readthedocs.io/) and the changes for the upcoming release can be found in <https://github.com/twisted/my-project/tree/main/changelog.d/>.

   <!-- towncrier release notes start -->


   EOF

.. note::

   The two empty lines at the end are on purpose.

That's it!
You can start adding news fragments:

.. code-block:: console

   towncrier create -c "Added a cool feature!" 1.added.md
   towncrier create -c "Changed a behavior!" 2.changed.md
   towncrier create -c "Deprecated a module!" 3.deprecated.md
   towncrier create -c "Removed a square feature!" 4.removed.md
   towncrier create -c "Fixed a bug!" 5.fixed.md
   towncrier create -c "Fixed a security issue!" 6.security.md
   towncrier create -c "Fixed a security issue!" 7.security.md
   towncrier create -c "A fix without an issue number!" +something-unique.fixed.md


After running ``towncrier build --yes --version 1.0.0`` (you can ignore the Git error messages) your ``CHANGELOG.md`` looks like this:

.. code-block:: markdown

   # Changelog

   All notable changes to this project will be documented in this file.

   The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

   This project uses [*towncrier*](https://towncrier.readthedocs.io/) and the changes for the upcoming release can be found in <https://github.com/twisted/my-project/tree/main/changelog.d/>.

   <!-- towncrier release notes start -->

   ## [1.0.0](https://github.com/twisted/my-project/tree/1.0.0) - 2022-09-28


   ### Security

   - Fixed a security issue! [#6](https://github.com/twisted/my-project/issues/6), [#7](https://github.com/twisted/my-project/issues/7)


   ### Removed

   - Removed a square feature! [#4](https://github.com/twisted/my-project/issues/4)


   ### Deprecated

   - Deprecated a module! [#3](https://github.com/twisted/my-project/issues/3)


   ### Added

   - Added a cool feature! [#1](https://github.com/twisted/my-project/issues/1)


   ### Changed

   - Changed a behavior! [#2](https://github.com/twisted/my-project/issues/2)


   ### Fixed

   - Fixed a bug! [#5](https://github.com/twisted/my-project/issues/5)
   - A fix without an issue number!

Pretty close, so this concludes this guide!

.. note::

   - The sections are rendered in the order the fragment types are defined.
   - Because ``towncrier`` doesn't have a concept of a "previous version" (yet), the version links will point to the release tags and not to the ``compare`` link like in *Keep a Changelog*.
   - *Keep a Changelog* doesn't have the concept of a uncategorized change, so the template doesn't expect any.
