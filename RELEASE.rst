Release Process
===============

..  note::
    Commands are written with Linux in mind and a ``venv`` located in ``venv/``.
    Adjust per your OS and virtual environment location.
    For example, on Windows with an environment in the directory ``myenv/`` the Python command would be ``myenv/scripts/python``.

Towncrier uses `CalVer <https://calver.org/>`_ of the form ``YY.MM.micro`` with the micro version just incrementing.

Before the final release, a set of release candidates are released.


Release candidate
-----------------

Create a release branch with a name of the form ``release-19.9.0`` starting from the main branch.
The same branch is used for the release candidate and the final release.
In the end, the release branch is merged into the main branch.

Update the version to the release candidate with the first being ``rc1`` (as opposed to 0).
In ``pyproject.toml`` the version is set using a PEP440 compliant string:

    version = "19.9.0rc1"

Use `towncrier` to generate the news release NEWS file, but first,
make sure the new version is installed::

    venv/bin/pip install -e .
    venv/bin/towncrier build --yes

Commit and push to the primary repository, not a fork.
It is important to not use a fork so that pushed tags end up in the primary repository,
server provided secrets for publishing to PyPI are available, and maybe more.

Create a PR named in the form ``Release 19.9.0``.
The same PR will be used for the release candidates and the final release.

Wait for the tests to be green.
Start with the release candidates.
Create a new release candidate using `GitHub New release UI <https://github.com/twisted/towncrier/releases/new>`_.

* *Choose a tag*: Type `19.9.0rc1` and select `Create new tag on publish.`
* *Target*: Search for the release branch and select it.
* *Title*: "Towncrier 19.9.0rc1".
* Set the content based on the NEWS file (for now in RST format).
* Make sure to check **This is a pre-release**.
* Click `Publish release`

This will trigger the PyPI release candidate.

Wait for the PyPI version to be published and then request a review for the PR from the ``twisted/twisted-contributors`` team.

In the PR request, you can give the link to the PyPI download and the documentation pages.
The documentation link is also available as part of the standard Read The Docs PR checks.

Notify the release candidate over IRC or Gitter to gain more attention.
In the PR comments, you can also mention anyone who has asked for a release.

We don't create discussion for pre-releases.
Any discussions before the final release, can go on the PR itself.

For now, the GitHub release text is reStructuredText as it's easy to copy and paste.
In the future we might create a separate Markdown version.


Release candidate publish failures
----------------------------------

The PyPI publish process is automatically triggered when a tag is created.

The publish is skipped for PRs, so we can check that the automated process works only a release time.
It can happen for the automated publish process to fail.

As long as the package was not published to PyPI, do the followings:

* Manually delete the candidate release from GitHub releases
* Manually delete the tag for the release candidate

Try to fix the issue and trigger the same release candidate again.

Once the package is published on PyPI, do not delete the release or the tag.
Proceed with create a new release candidate instead.


Final release
-------------

Once the PR is approved, you can trigger the final release.

Update the version to the final version.
In ``pyproject.toml`` the version is set using a PEP440 compliant string:

    version = "19.9.0"

Manually update the `NEWS.rst` file to include the final release version and date.
Usually it will look like this.
This will replace the release candidate section::

    towncrier 19.9.0 (2019-09-01)
    =============================

    No significant changes since the previous release candidate.

Commit and push the change.
Wait for the tests to be green.

Trigger the final release using GitHub Release GUI.

Similar to the release candidate, with the difference:

* tag will be named `19.9.0`
* the target is the same branch
* Title will be `towncrier 19.9.0`
* Content can be the content of the final release (RST format).
* Check **Set as the latest release**.
* Check **Create a discussion for this release**.
* Click `Publish release`

No need for another review request.

Update the version to the development version.
In ``pyproject.toml`` the version is set using a PEP440 compliant string:

    version = "19.9.0.dev0"

Commit and push the changes.

Merge the commit in the main branch, **without using squash**.

We tag the release based on a commit from the release branch.
If we merge with squash,
the release tag commit will no longer be found in the main branch history.
With a squash merge, the whole branch history is lost.
This causes the `pre-commit autoupdate` to fail.
See `PR590 <https://github.com/twisted/towncrier/pull/590>`_ for more details.

You can announce the release over IRC, Gitter, or Twisted mailing list.

Done.
