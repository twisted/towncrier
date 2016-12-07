# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
from twisted.trial.unittest import TestCase

from click.testing import CliRunner
from .. import _main


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

            result = runner.invoke(_main, ['--draft'])

        if result.exception:
            print(result.output)
            raise result.exception

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            u'Loading template...\nFinding news fragments...\nRendering news '
            u'fragments...\nDraft only -- nothing has been written.\nWhat is '
            u'seen below is what would be written.\n\nFoo 1.2.3\n==========\n'
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

            result = runner.invoke(_main, ['--draft'])

        if result.exception:
            print(result.output)
            print(result.exception)
            raise result.exception

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            u'Loading template...\nFinding news fragments...\nRendering news '
            u'fragments...\nDraft only -- nothing has been written.\nWhat is '
            u'seen below is what would be written.\n\nFoo 1.2.3\n==========\n'
            u'\n\nFeatures\n--------\n\n- Adds levitation (#123)\n\n'
        )
