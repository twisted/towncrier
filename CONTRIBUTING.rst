Contributing to Towncrier
=========================

Want to contribute to this project? Great! We'd love to hear from you!

As a developer and user, you probably have some questions about our project and how to contribute.
In this article, we try to answer these and give you some recommendations.


Ways to communicate and contribute
----------------------------------

There are several options to contribute to this project:

* Open a new topic on our  `GitHub Discussions`_ page.

  Tell us about your ideas or ask questions there.
  Discuss with us the next Towncrier release.

* Help or comment on our GitHub `issues`_ tracker.

  There are certainly many issues where you can help with your expertise.
  Or you would like to share your ideas with us.

* Open a new issue using GitHub `issues`_ tracker.

  If you found a bug or have a new cool feature, describe your findings.
  Try to be as descriptive as possible to help us understand your issue.

* Check out the Libera ``#twisted`` IRC channel or `Twisted Gitter <https://gitter.im/twisted/twisted>`_.

  If you prefer to discuss some topics personally,
  you may find the IRC or Gitter channels interesting.
  They are bridged.

* Modify the code.

  If you would love to see the new feature in the next release, this is probably the best way.


Modifying the code
------------------

The source code is managed using Git and is hosted on GitHub::

    https://github.com/twisted/towncrier
    git@github.com:twisted/towncrier.git


We recommend the following workflow:

#. `Fork our project <https://github.com/twisted/towncrier/fork>`_ on GitHub.

#. Clone your forked Git repository (replace ``GITHUB_USER`` with your
   account name on GitHub)::

   $ git clone git@github.com:GITHUB_USER/towncrier.git

#. Prepare a pull request:

   a. Create a new branch with::

      $ git checkout -b <BRANCH_NAME>

   b. Write your test cases and run the complete test suite, see the section
      *Running the test suite* for details.

   c. Document any user-facing changes in one of the ``/docs/`` files.
      Use `one sentence per line`_.

   d. Create a news fragment in ``src/towncrier/newsfragments/`` describing the changes and containing information that is of interest to end-users.
      Use `one sentence per line`_ here, too.
      You can use the ``towncrier`` CLI to create them; for example ``towncrier create 1234.bugfix``

      Use one of the following types:

      - ``feature`` for new features
      - ``bugfix`` for bugfixes
      - ``doc`` for improvements to documentation
      - ``removal`` for deprecations and removals
      - ``misc`` for everything else that is linked but not shown in our ``NEWS.rst`` file.
        Use this for pull requests that don't affect end-users and leave them empty.

   e. Create a `pull request`_.
      Describe in the pull request what you did and why.
      If you have open questions, ask.
      (optional) Allow team members to edit the code on your PR.

#. Wait for feedback. If you receive any comments, address these.

#. After your pull request is merged, delete your branch.


.. _testsuite:

Running the test suite
----------------------

We use the `twisted.trial`_ module and `nox`_ to run tests against all supported
Python versions and operating systems.

The following list contains some ways how to run the test suite:

* To install this project into a virtualenv along with the dependencies necessary
  to run the tests and build the documentation::

    $ pip install -e .[dev]

* To run the tests, use ``trial`` like so::

    $ trial towncrier

* To investigate and debug errors, use the ``trial`` command like this::

    $ trial -b towncrier

  This will invoke a PDB session. If you press ``c`` it will continue running
  the test suite until it runs into an error.

* To run all tests against all supported versions, install nox and use::

    $ nox

  You may want to add the ``--no-error-on-missing-interpreters`` option to avoid errors
  when a specific Python interpreter version couldn't be found.

*  To get a complete list of the available targets, run::

    $ nox -l

* To run only a specific test only, use the ``towncrier.test.FILE.CLASS.METHOD`` syntax,
  for example::

    $ nox -e tests -- towncrier.test.test_project.InvocationTests.test_version

* To run some quality checks before you create the pull request,
  we recommend using this call::

    $ nox -e pre_commit check_newsfragment

* Or enable `pre-commit` as a git hook::

    $ pip install pre-commit
    $ pre-commit install


**Please note**: If the test suite works in nox, but doesn't by calling
``trial``, it could be that you've got GPG-signing active for git commits which
fails with our dummy test commits.

.. ### Links

.. _flake8: https://flake8.pycqa.org/
.. _GitHub Discussions: https://github.com/twisted/towncrier/discussions
.. _issues:  https://github.com/twisted/towncrier/issues
.. _pull request: https://github.com/twisted/towncrier/pulls
.. _nox: https://nox.thea.codes/
.. _`one sentence per line`: https://rhodesmill.org/brandon/2012/one-sentence-per-line/
.. _twisted.trial: https://github.com/twisted/trac-wiki-archive/blob/trunk/TwistedTrial.mediawiki
