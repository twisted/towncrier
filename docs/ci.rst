CI/CD Pipelines
===============

``towncrier`` can be integrated into your CI/CD pipeline to automatically
check that news fragments are present and to build the changelog as part of
your release process.

This page covers the two most common CI/CD platforms: GitHub Actions and
GitLab CI.


GitHub Actions
--------------

Checking news fragments in pull requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most common use case is to check that every pull request includes at least
one news fragment.  The following workflow runs ``towncrier check`` on every
pull request:

.. code-block:: yaml

    # .github/workflows/ci.yml
    name: CI

    on:
      push:
        branches: [ main ]
      pull_request:

    jobs:
      check-newsfragment:
        name: Check news fragment
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
            with:
              fetch-depth: 0

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: "3.x"

          - name: Install towncrier
            run: python -m pip install towncrier

          - name: Check for news fragment
            run: |
              git fetch origin ${{ github.base_ref }}
              towncrier check --compare-with origin/${{ github.base_ref }}

.. note::

    ``towncrier check`` compares the current branch against a base branch
    (``origin/main`` by default).  Make sure your workflow checks out the
    full git history with ``fetch-depth: 0`` so the comparison works
    correctly.

Building the changelog in CI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also build the changelog as part of a release workflow.  The
following example builds the changelog and uploads it as an artifact:

.. code-block:: yaml

    # .github/workflows/release.yml
    name: Release

    on:
      push:
        tags:
          - "v*"

    jobs:
      build-changelog:
        name: Build changelog
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: "3.x"

          - name: Install towncrier
            run: python -m pip install towncrier

          - name: Build changelog
            run: towncrier build --yes --version "${GITHUB_REF#refs/tags/v}"

          - name: Upload changelog
            uses: actions/upload-artifact@v4
            with:
              name: changelog
              path: |
                NEWS.rst
                CHANGELOG.rst


GitLab CI
---------

Checking news fragments in merge requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following ``.gitlab-ci.yml`` snippet checks that every merge request
includes at least one news fragment:

.. code-block:: yaml

    # .gitlab-ci.yml
    stages:
      - test

    check-newsfragment:
      stage: test
      image: python:3-slim
      before_script:
        - python -m pip install towncrier
      script:
        - towncrier check --compare-with origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME
      rules:
        - if: $CI_PIPELINE_SOURCE == "merge_request_event"

.. note::

    ``towncrier check`` compares the current branch against a base branch
    (``origin/main`` by default).  In the example above we use the GitLab CI
    variable ``$CI_MERGE_REQUEST_TARGET_BRANCH_NAME`` to compare against the
    target branch of the merge request.

Building the changelog in CI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can build the changelog as part of a release pipeline.  The following
example builds the changelog and stores it as a build artifact:

.. code-block:: yaml

    # .gitlab-ci.yml
    stages:
      - build

    build-changelog:
      stage: build
      image: python:3-slim
      before_script:
        - python -m pip install towncrier
      script:
        - towncrier build --yes --version "$CI_COMMIT_TAG"
      artifacts:
        paths:
          - NEWS.rst
          - CHANGELOG.rst
      rules:
        - if: $CI_COMMIT_TAG


Using pre-commit in CI
----------------------

If you already use ``pre-commit`` (see :doc:`pre-commit`), you can also run
the ``towncrier-check`` hook in your CI pipeline.  This is useful if you want
to enforce news fragment checks without adding a separate CI step.

For GitHub Actions:

.. code-block:: yaml

    - name: Run pre-commit
      run: |
        python -m pip install pre-commit
        pre-commit run --all-files

For GitLab CI:

.. code-block:: yaml

    pre-commit:
      stage: test
      image: python:3-slim
      before_script:
        - python -m pip install pre-commit
      script:
        - pre-commit run --all-files
