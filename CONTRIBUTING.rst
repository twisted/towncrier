Releasing
=========

Summary
-------

- Create a release branch in the main repository, not in a fork.
- Prepare a commit for a release candidate, get an approving review, and tag the commit which will upload artifacts to PyPI.
- Notify people and give time for feedback.
- Address concerns raised via new issues for later handling or PRs against the release branch.
- Prepare a commit for a final release, get an approving review, and tag the commit which will upload artifacts to PyPI.


Step-by-step
------------

.. note::

    Commands are written with Linux in mind and a ``venv`` located in ``venv/``.
    Adjust per your OS and virtual environment location.
    For example, on Windows with an environment in the directory ``myenv/`` the Python command would be ``myenv/scripts/python``.

- Define the final release version you are preparing.

  - towncrier uses `CalVer <https://calver.org/>`_ of the form ``YY.MM.micro`` with the micro version just incrementing.
  - Normalize the version according to `PEP 440 <https://www.python.org/dev/peps/pep-0440/#normalization>`_.

    - This requires that ``towncrier[dev]`` extra is installed.
    - ``venv/bin/python admin/canonicalize_version.py 19.09.00-rc1``
    - Outputs ``19.9rc1`` which is the form to be used.

- Create a release branch with a name of the form ``release-19.9`` starting from the ``master`` branch.

  - This new branch will contain all tagged release candidate commits as well as the final tagged release commit.

- Update the version to the release candidate with the first being ``rc1`` (as opposed to 0).

  - In ``src/towncrier/_version.py`` the version is set using ``incremental`` such as ``__version__ = Version('towncrier', 19, 9, release_candidate=1)``

- Run ``venv/bin/towncrier build --yes`` to build the the newsfragments into the release notes document and remove the newsfragment files.

- Commit and push to the primary repository, not a fork.

  - It is important to not use a fork so that pushed tags end up in the primary repository.

- If working on the first release candidate from this branch, create a PR named in the form ``Release 19.9``.

- Request a review and address raised concerns until receiving an approval.

- Tag that commit such as ``19.9rc1`` and push the tag to the primary repository.

  - This will result in another build which will publish to PyPI.
  - Confirm the presence of the release on PyPI.
  - # TODO: use the GitHub release and tagging feature?

- If not processing the final release, `dismiss the approving review <https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/dismissing-a-pull-request-review>`_.

  - The review process will be reused for any subsequent release candidates as well as the final release so it must be cleared at each stage.

- # TODO: notify people some how some way, the maillist?  hmmm...

- If another release candidate is required:

  - Submit PRs against the release branch to integrate the needed changes.

  - Return to the step where the version is updated and increment the release candidate number.

- If ready for a final release, remove the release candidate indicator from the version.

  - Edit ``src/towncrier/_version.py`` such as ``__version__ = Version('towncrier', 19, 9)`` to remove the release candidate indication.

  - Return to the towncrier build step and continue.

- Once the final release has been made, leave the approving review intact and merge the PR.

# TODO: should we have an indicator on the version for interrim development or just leave the last release version intact?
