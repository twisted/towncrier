# Copyright (c) Amber Brown, 2015
# See LICENSE for details.
import os
from subprocess import call
from contextlib import contextmanager

from twisted.trial.unittest import TestCase

from click.testing import CliRunner
from .. import _main


@contextmanager
def setup_simple_project():
    with open('pyproject.toml', 'w') as f:
        f.write(
            '[tool.towncrier]\n'
            'package = "foo"\n'
        )
    os.mkdir('foo')
    with open('foo/__init__.py', 'w') as f:
        f.write('__version__ = "1.2.3"\n')
    os.mkdir('foo/newsfragments')


class TestCli(TestCase):

    maxDiff = None

    def test_happy_path(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open('pyproject.toml', 'w') as f:
                f.write(
                    '[tool.towncrier]\n'
                    'package = "foo"\n'
                )
            os.mkdir('foo')
            with open('foo/__init__.py', 'w') as f:
                f.write('__version__ = "1.2.3"\n')
            os.mkdir('foo/newsfragments')
            with open('foo/newsfragments/123.feature', 'w') as f:
                f.write('Adds levitation')
            # Towncrier ignores .rst extension
            with open('foo/newsfragments/124.feature.rst', 'w') as f:
                f.write('Extends levitation')

            result = runner.invoke(_main, ['--draft', '--date', '01-01-2001'])

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            u'Loading template...\nFinding news fragments...\nRendering news '
            u'fragments...\nDraft only -- nothing has been written.\nWhat is '
            u'seen below is what would be written.\n\nFoo 1.2.3 (01-01-2001)'
            u'\n======================\n'
            u'\n\nFeatures\n--------\n\n- Adds levitation (#123)\n'
            u'- Extends levitation (#124)\n\n'
        )

    def test_sorting(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project()
            with open('foo/newsfragments/123.feature', 'w') as f:
                f.write('Adds levitation')

            result = runner.invoke(_main, ['--draft', '--date', '01-01-2001'])

        # Issues should be sorted alphabetic before

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            u'Loading template...\nFinding news fragments...\nRendering news '
            u'fragments...\nDraft only -- nothing has been written.\nWhat is '
            u'seen below is what would be written.\n\nFoo 1.2.3 (01-01-2001)'
            u'\n======================\n'
            u'\n\nFeatures\n--------\n\n- Adds levitation (#123)\n\n'
        )

    def test_no_confirmation(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open('pyproject.toml', 'w') as f:
                f.write(
                    '[tool.towncrier]\n'
                    'package = "foo"\n'
                )
            os.mkdir('foo')
            with open('foo/__init__.py', 'w') as f:
                f.write('__version__ = "1.2.3"\n')
            os.mkdir('foo/newsfragments')
            fragment_path = 'foo/newsfragments/123.feature'
            with open(fragment_path, 'w') as f:
                f.write('Adds levitation')

            call(["git", "init"])
            call(["git", "config", "user.name", "user"])
            call(["git", "config", "user.email", "user@example.com"])
            call(["git", "add", "."])
            call(["git", "commit", "-m", "Initial Commit"])

            result = runner.invoke(_main, ['--date', '01-01-2001', '--yes'])

            self.assertEqual(0, result.exit_code)
            path = 'NEWS.rst'
            self.assertTrue(os.path.isfile(path))
            self.assertFalse(os.path.isfile(fragment_path))
