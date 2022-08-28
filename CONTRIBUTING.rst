Contributing to Towncrier
=========================

Want to contribute to this project? Great! We'd love to hear from you!

As a developer and user, you probably have some questions about our
project and how to contribute.
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

  If you would love to see the new feature in the next release, this is
  probably the best way.


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

   d. Create a newsfragment in ``src/towncrier/newsfragments/`` describing the changes and containing information that is of interest to end-users.

   e. Create a `pull request`_.
      Describe in the pull request what you did and why.
      If you have open questions, ask.
      (optional) Allow team members to edit the code on your PR.

#. Wait for feedback. If you receive any comments, address these.

#. After your pull request is merged, delete your branch.


.. _testsuite:

Running the test suite
----------------------

We use the `twisted.trial`_ module and `tox`_ to run tests against all supported
Python versions and operating systems. All test dependencies, other than tox, are installed
automatically.

The following list contains some ways how to run the test suite:

* To run all tests, use::

    $ tox

  You may want to add the ``--skip-missing-interpreters`` option to avoid errors
  when a specific Python interpreter version couldn't be found.

*  To get a complete list of the available targets, run::

    $ tox -av

* To run only a specific test only, use the ``towncrier.test.FILE.CLASS.METHOD`` syntax,
  for example::

    $ tox -- towncrier.test.test_project.InvocationTests.test_version

* To run some quality checks before you create the pull request,
  we recommend using this call::

    $ tox -e pre-commit,check-manifest,check-newsfragment

* Or enable `pre-commit` as a git hook::

    $ pip install pre-commit
    $ pre-commit install

* To investigate and debug errors, use the ``trial`` command like this::

    $ trial -b towncrier

  This command creates a virtual environment and invokes a PDB session.


.. ### Links

.. _flake8: https://flake8.rtfd.io
.. _GitHub Discussions: https://github.com/twisted/towncrier/discussions
.. _issues:  https://github.com/twisted/towncrier/issues
.. _pull request: https://github.com/twisted/towncrier/pulls
.. _tox: https://tox.rtfd.org/
.. _twisted.trial: https://twistedmatrix.com/trac/wiki/TwistedTrial
