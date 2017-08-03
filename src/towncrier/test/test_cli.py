# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
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

    def test_happy_path_ini(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open('towncrier.ini', 'w') as f:
                f.write(
                    '[towncrier]\n'
                    'package = foo\n'
                    'package_dir = .\n'
                )
            os.mkdir('foo')
            with open('foo/__init__.py', 'w') as f:
                f.write('__version__ = "1.2.3"\n')
            os.mkdir('foo/newsfragments')
            with open('foo/newsfragments/123.feature', 'w') as f:
                f.write('Adds levitation')

            result = runner.invoke(_main, ['--draft', '--date', '01-01-2001'])

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            u'Loading template...\nFinding news fragments...\nRendering news '
            u'fragments...\nDraft only -- nothing has been written.\nWhat is '
            u'seen below is what would be written.\n\nFoo 1.2.3 (01-01-2001)'
            u'\n======================\n'
            u'\n\nFeatures\n--------\n\n- Adds levitation (#123)\n\n'
        )

    def test_happy_path_toml(self):
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

            result = runner.invoke(_main, ['--draft', '--date', '01-01-2001'])

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            u'Loading template...\nFinding news fragments...\nRendering news '
            u'fragments...\nDraft only -- nothing has been written.\nWhat is '
            u'seen below is what would be written.\n\nFoo 1.2.3 (01-01-2001)'
            u'\n======================\n'
            u'\n\nFeatures\n--------\n\n- Adds levitation (#123)\n\n'
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
