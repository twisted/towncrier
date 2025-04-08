Customizing the News File Output
================================

Adding Content Above ``towncrier``
----------------------------------

If you wish to have content at the top of the news file (for example, to say where you can find the issues), you can use a special rST comment to tell ``towncrier`` to only update after it.
In your existing news file (e.g. ``NEWS.rst``), add the following line above where you want ``towncrier`` to put content:

.. code-block:: restructuredtext

    .. towncrier release notes start

In an existing news file, it'll look something like this:

.. code-block:: restructuredtext

    This is the changelog of my project. You can find the
    issue tracker at http://blah.

    .. towncrier release notes start

    myproject 1.0.2 (2018-01-01)
    ============================

    Bugfixes
    --------

    - Fixed, etc...

``towncrier`` will not alter content above the comment.

Markdown
~~~~~~~~

If your news file is in Markdown (e.g. ``NEWS.md``), use the following comment instead:

.. code-block:: html

    <!-- towncrier release notes start -->


Adding Content at the Start of the Next Release
-----------------------------------------------

Using a custom section type, you can add content at the start of the next release.
Here's an example configuration to add a text-only section at the start of the next release:

.. code-block:: toml

   [[tool.towncrier.type]]
   name = ""
   directory = "highlight"
   all_bullets = false
   check = false

   [[tool.towncrier.type]]
   use_default_types = true

Any fragments with a suffix of ``.highlight`` will be added to this highlight section which will be rendered as the first section after the release title (with no title of its own).
The section has no visible name and no bullets, so the content of the fragments will be shown directly after the release title (or in the case of a more complex configuration with multiple sections, after the relevant section title).

The output of the above configuration with a ``+.highlight.rst`` fragment containing "Happy new year!" (and other ``.feature`` fragments) will look something like this:

.. code-block:: rst

   myproject 1.2.3 (2026-01-01)
   ============================


   Happy new year!


   Features
   --------

   - Added, etc...
