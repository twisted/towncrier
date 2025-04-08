import os

from textwrap import dedent

from twisted.trial.unittest import TestCase

from .._builder import render_fragments, split_fragments
from .._settings import load_config
from .helpers import read_pkg_resource, write


class BulletsTests(TestCase):
    maxDiff = None

    def mktemp_project(
        self, *, pyproject_toml: str = "", towncrier_toml: str = ""
    ) -> str:
        """
        Create a temporary directory with config files.
        """
        project_dir = self.mktemp()
        os.makedirs(project_dir)

        if pyproject_toml:
            write(
                os.path.join(project_dir, "pyproject.toml"),
                pyproject_toml,
                dedent=True,
            )

        if towncrier_toml:
            write(
                os.path.join(project_dir, "towncrier.toml"),
                towncrier_toml,
                dedent=True,
            )

        return project_dir

    def test_render_rst_all_bullets_true_default(self):
        """
        Default behavior: all_bullets is True, RST renders with bullets.
        """
        project_dir = self.mktemp_project(
            pyproject_toml="""
                [tool.towncrier]
                package = "foobar"
                filename = "NEWS.rst"
                # all_bullets defaults to true
                [tool.towncrier.fragment.feat]
                name = "Features"
                [tool.towncrier.fragment.fix]
                name = "Bugfixes"
            """
        )
        config = load_config(project_dir)
        assert config is not None  # Assure type checker
        template_resource_path = f"templates/{config.template[1]}"
        template_content = read_pkg_resource(template_resource_path)
        raw_fragments = {
            "": {
                ("1", "feat", 0): "Feature 1.",
                ("2", "fix", 0): "Fix 2.",
            },
        }
        processed_fragments = split_fragments(
            raw_fragments, config.types, config.all_bullets
        )
        rendered = render_fragments(
            template=template_content,
            issue_format=config.issue_format,
            fragments=processed_fragments,
            definitions=config.types,
            underlines=config.underlines[1:],
            wrap=config.wrap,
            versiondata={"name": "MyProject", "version": "1.0", "date": "never"},
            all_bullets=config.all_bullets,
            render_title=False,  # Don't render title in fragment tests
        )
        expected = """
Features
--------

- Feature 1. (#1)


Bugfixes
--------

- Fix 2. (#2)

"""
        self.assertEqual(dedent(expected).strip(), rendered.strip())

    def test_render_rst_all_bullets_false_global(self):
        """
        Global all_bullets=false, RST renders without bullets.
        """
        project_dir = self.mktemp_project(
            pyproject_toml="""
                [tool.towncrier]
                package = "foobar"
                filename = "NEWS.rst"
                all_bullets = false
                [tool.towncrier.fragment.feat]
                name = "Features"
                [tool.towncrier.fragment.fix]
                name = "Bugfixes"
            """
        )
        config = load_config(project_dir)
        assert config is not None  # Assure type checker
        template_resource_path = f"templates/{config.template[1]}"
        template_content = read_pkg_resource(template_resource_path)
        raw_fragments = {
            "": {
                ("1", "feat", 0): "Feature 1.",
                ("2", "fix", 0): "Fix 2.",
            },
        }
        processed_fragments = split_fragments(
            raw_fragments, config.types, config.all_bullets
        )
        rendered = render_fragments(
            template=template_content,
            issue_format=config.issue_format,
            fragments=processed_fragments,
            definitions=config.types,
            underlines=config.underlines[1:],
            wrap=config.wrap,
            versiondata={"name": "MyProject", "version": "1.0", "date": "never"},
            all_bullets=config.all_bullets,
            render_title=False,  # Don't render title in fragment tests
        )
        expected = """
Features
--------

Feature 1. (#1)


Bugfixes
--------

Fix 2. (#2)

"""
        self.assertEqual(dedent(expected).strip(), rendered.strip())

    def test_render_rst_all_bullets_override(self):
        """
        Per-category all_bullets overrides global setting in RST.
        """
        project_dir = self.mktemp_project(
            pyproject_toml="""
                [tool.towncrier]
                package = "foobar"
                filename = "NEWS.rst"
                all_bullets = false # Global false
                [tool.towncrier.fragment.feat]
                name = "Features"
                all_bullets = true # Override to true
                [tool.towncrier.fragment.fix]
                name = "Bugfixes"
                # Inherits global false
                [tool.towncrier.fragment.fish]
                name = "Docs"
                all_bullets = false # Explicit false
            """
        )
        config = load_config(project_dir)
        assert config is not None  # Assure type checker
        template_resource_path = f"templates/{config.template[1]}"
        template_content = read_pkg_resource(template_resource_path)
        raw_fragments = {
            "": {
                ("1", "feat", 0): "Feature 1.",
                ("2", "fix", 0): "Fix 2.",
                ("3", "fish", 0): "Doc 3.",
            },
        }
        processed_fragments = split_fragments(
            raw_fragments, config.types, config.all_bullets
        )
        rendered = render_fragments(
            template=template_content,
            issue_format=config.issue_format,
            fragments=processed_fragments,
            definitions=config.types,
            underlines=config.underlines[1:],
            wrap=config.wrap,
            versiondata={"name": "MyProject", "version": "1.0", "date": "2026-01-01"},
            all_bullets=config.all_bullets,
        )
        # Note: Order is sorted based on alphabetical fragment names
        expected = """
MyProject 1.0 (2026-01-01)
==========================

Features
--------

- Feature 1. (#1)


Docs
----

Doc 3. (#3)


Bugfixes
--------

Fix 2. (#2)


"""
        self.assertEqual(dedent(expected).strip(), rendered.strip())

    def test_render_md_all_bullets_true_default(self):
        """
        Default behavior: all_bullets is True, Markdown renders with bullets.
        """
        project_dir = self.mktemp_project(
            pyproject_toml="""
                [tool.towncrier]
                package = "foobar"
                filename = "NEWS.md" # Triggers markdown template
                # all_bullets defaults to true
                [tool.towncrier.fragment.feat]
                name = "Features"
                [tool.towncrier.fragment.fix]
                name = "Bugfixes"
            """
        )
        config = load_config(project_dir)
        assert config is not None  # Assure type checker
        template_resource_path = f"templates/{config.template[1]}"
        template_content = read_pkg_resource(template_resource_path)
        raw_fragments = {
            "": {
                ("1", "feat", 0): "Feature 1.",
                ("2", "fix", 0): "Fix 2.",
            },
        }
        processed_fragments = split_fragments(
            raw_fragments, config.types, config.all_bullets
        )
        rendered = render_fragments(
            template=template_content,
            issue_format=config.issue_format,
            fragments=processed_fragments,
            definitions=config.types,
            underlines=config.underlines[1:],
            wrap=config.wrap,
            versiondata={"name": "MyProject", "version": "1.0", "date": "never"},
            all_bullets=config.all_bullets,
            render_title=False,  # Don't render title in fragment tests
        )
        expected = """
## Features

- Feature 1. (#1)

## Bugfixes

- Fix 2. (#2)

"""
        self.assertEqual(dedent(expected).strip(), rendered.strip())

    def test_render_md_all_bullets_false_global(self):
        """
        Global all_bullets=false, Markdown renders without bullets.
        """
        project_dir = self.mktemp_project(
            pyproject_toml="""
                [tool.towncrier]
                package = "foobar"
                filename = "NEWS.md"
                all_bullets = false
                [tool.towncrier.fragment.feat]
                name = "Features"
                [tool.towncrier.fragment.fix]
                name = "Bugfixes"
            """
        )
        config = load_config(project_dir)
        assert config is not None  # Assure type checker
        template_resource_path = f"templates/{config.template[1]}"
        template_content = read_pkg_resource(template_resource_path)
        raw_fragments = {
            "": {
                ("1", "feat", 0): "Feature 1.",
                ("2", "fix", 0): "Fix 2.",
            },
        }
        processed_fragments = split_fragments(
            raw_fragments, config.types, config.all_bullets
        )
        rendered = render_fragments(
            template=template_content,
            issue_format=config.issue_format,
            fragments=processed_fragments,
            definitions=config.types,
            underlines=config.underlines[1:],
            wrap=config.wrap,
            versiondata={},
            all_bullets=config.all_bullets,
            render_title=False,  # Don't render title in fragment tests
        )
        expected = """
## Features

Feature 1. (#1)

## Bugfixes

Fix 2. (#2)

"""
        self.assertEqual(dedent(expected).strip(), rendered.strip())

    def test_render_md_all_bullets_override(self):
        """
        Per-category all_bullets overrides global setting in Markdown.
        """
        project_dir = self.mktemp_project(
            pyproject_toml="""
                [tool.towncrier]
                package = "foobar"
                filename = "NEWS.md"
                all_bullets = true # Global true
                [tool.towncrier.fragment.feat]
                name = "Features"
                # Inherits global true
                [tool.towncrier.fragment.fix]
                name = "Bugfixes"
                all_bullets = false # Override to false
                [tool.towncrier.fragment.fish]
                name = "Docs"
                all_bullets = true # Explicit true
            """
        )
        config = load_config(project_dir)
        assert config is not None  # Assure type checker
        template_resource_path = f"templates/{config.template[1]}"
        template_content = read_pkg_resource(template_resource_path)
        raw_fragments = {
            "": {
                ("1", "feat", 0): "Feature 1.",
                ("2", "fix", 0): "Fix 2.",
                ("3", "fish", 0): "Doc 3.",
            },
        }
        processed_fragments = split_fragments(
            raw_fragments, config.types, config.all_bullets
        )
        rendered = render_fragments(
            template=template_content,
            issue_format=config.issue_format,
            fragments=processed_fragments,
            definitions=config.types,
            underlines=config.underlines[1:],
            wrap=config.wrap,
            versiondata={},  # MD template might not need versiondata for title
            all_bullets=config.all_bullets,
            render_title=False,  # Don't render title in fragment tests
        )
        # Note: Order is sorted based on alphabetical fragment names
        expected = """
## Features

- Feature 1. (#1)

## Docs

- Doc 3. (#3)

## Bugfixes

Fix 2. (#2)

"""
        self.assertEqual(dedent(expected).strip(), rendered.strip())

    def test_render_rst_all_bullets_array_format(self):
        """
        Per-category all_bullets overrides global setting using the array format.
        """
        project_dir = self.mktemp_project(
            pyproject_toml="""
                [tool.towncrier]
                package = "foobar"
                filename = "NEWS.rst"
                all_bullets = false # Global false

                [[tool.towncrier.type]]
                directory = "feat"
                name = "Features"
                all_bullets = true # Override to true

                [[tool.towncrier.type]]
                directory = "fix"
                name = "Bugfixes"
                # Inherits global false

                [[tool.towncrier.type]]
                directory = "docs"
                name = "Documentation"
                all_bullets = false # Explicit false
            """
        )
        config = load_config(project_dir)
        assert config is not None
        template_resource_path = f"templates/{config.template[1]}"
        template_content = read_pkg_resource(template_resource_path)
        raw_fragments = {
            "": {
                ("1", "feat", 0): "Feature 1.",
                ("2", "fix", 0): "Fix 2.",
                ("3", "docs", 0): "Doc 3.",
            },
        }
        processed_fragments = split_fragments(
            raw_fragments, config.types, config.all_bullets
        )
        rendered = render_fragments(
            template=template_content,
            issue_format=config.issue_format,
            fragments=processed_fragments,
            definitions=config.types,
            underlines=config.underlines[1:],
            wrap=config.wrap,
            versiondata={"name": "MyProject", "version": "1.0", "date": "2026-01-01"},
            all_bullets=config.all_bullets,
        )
        # Order is sorted based on the order of the array
        expected = """
MyProject 1.0 (2026-01-01)
==========================

Features
--------

- Feature 1. (#1)


Bugfixes
--------

Fix 2. (#2)


Documentation
-------------

Doc 3. (#3)

"""
        self.assertEqual(dedent(expected).strip(), rendered.strip())
