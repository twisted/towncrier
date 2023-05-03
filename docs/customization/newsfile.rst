Customizing the News File Output
================================

Adding Content Above ``towncrier``
----------------------------------

If you wish to have content at the top of the news file (for example, to say where you can find the tickets), you can use a special rST comment to tell ``towncrier`` to only update after it.
In your existing news file (e.g. ``NEWS.rst``), add the following line above where you want ``towncrier`` to put content::

  .. towncrier release notes start

In an existing news file, it'll look something like this::

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

If your news file is in Markdown (e.g. ``NEWS.md``), use the following comment instead::

  <!--- towncrier release notes start -->
