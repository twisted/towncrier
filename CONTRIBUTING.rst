Releasing
=========

Summary
-------

- Create a release branch in the main repository, not in a fork.
- Create a commit for a release candidate inside the release branch.
- Create a Pull Request for the release. The same branch and PR will be used for both the release candidates and  the final release.
- Get an approving review.
- Once approved, tag the last commit in the branch as a release candidate.
- Push the tag.  This will trigger a build including the upload of artifacts to PyPI.
- Notify the Twisted maillist allow a week for feedback before continuing.
- Make sure that tickets exist for all raised concerns.  These tickets should be marked using the ``blocking`` label.
- Address each issue by either concluding that it is not really a release blocker and removing the label or by fixing via a PR to the release branch.
- Prepare a commit for a final release and push it to the release branch.
- Get an approving review for the final release.
- Tag the commit using the final release version. This will trigger the upload of artifacts to PyPI.


Step-by-step
------------

.. note::

    Commands are written with Linux in mind and a ``venv`` located in ``venv/``.
    Adjust per your OS and virtual environment location.
    For example, on Windows with an environment in the directory ``myenv/`` the Python command would be ``myenv/scripts/python``.

- Define the final release version you are preparing.

  - towncrier uses `CalVer <https://calver.org/>`_ of the form ``YY.MM.micro`` with the micro version just incrementing.
  - Normalize the version according to `incremental <https://github.com/twisted/incremental/>`_.

    - This requires that ``towncrier[dev]`` extra is installed.
    - ``venv/bin/python admin/canonicalize_version.py 19.09.00-rc1``
    - Outputs ``19.9.0.rc1`` which is the form to be used.

- Create a release branch with a name of the form ``release-19.9.0`` starting from the ``master`` branch.

  - On the new release branch you will commit all tagged release candidate commits as well as the final tagged release commit.

- Update the version to the release candidate with the first being ``rc1`` (as opposed to 0).

  - In ``src/towncrier/_version.py`` the version is set using ``incremental`` such as ``__version__ = Version('towncrier', 19, 9, 0, release_candidate=1)``

- Run ``venv/bin/towncrier build --yes`` to build the the newsfragments into the release notes document and to automatically remove the newsfragment files.

- Commit and push to the primary repository, not a fork.

  - It is important to not use a fork so that pushed tags end up in the primary repository, server provided secrets for publishing to PyPI are available, and maybe more.

- If working on the first release candidate from this branch, create a PR named in the form ``Release 19.9``.

- Request a review and address raised concerns until receiving an approval.

- Tag that commit such as ``19.9.0.rc1`` and push the tag to the primary repository.

  - This will result in another build which will publish to PyPI.
  - Confirm the presence of the release on PyPI.

- `Dismiss the approving review <https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/dismissing-a-pull-request-review>`_.

  - The review process will be reused for any subsequent release candidates, the final release, and the post-release tweaks so it must be cleared at each stage.

- Notify the `Twisted-Python maillist <https://twistedmatrix.com/cgi-bin/mailman/listinfo/twisted-python>`_ of the release to allow for feedback if a pre-release and just for notification if a final release.

- If another release candidate is required:

  - Submit PRs against the release branch to integrate the needed changes.  Any PRs could be cherry picks from the ``master`` branch if already resolved there, or direct PRs against the release branch that will be merged back into master at the completion of the release.

  - Return to the step where the version is updated and increment the release candidate number.

- If ready for a final release, remove the release candidate indicator from the version.

  - Edit ``src/towncrier/_version.py`` such as ``__version__ = Version('towncrier', 19, 9, 0)`` to remove the release candidate indication.

  - Return to the towncrier build step and continue.

- If the final release has been completed, continue below.

- Increment the patch version by one and set to a development version.

  - In ``src/towncrier/_version.py`` the version is set using ``incremental`` such as ``__version__ = Version('towncrier', 19, 9, 1, dev=0)``

- Merge without waiting for an approving review.
