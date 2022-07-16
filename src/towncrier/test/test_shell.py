#
# Tests for the high-level CLI command.
# Sub-commands are tested via separate test files.
#
from click.testing import CliRunner
from twisted.trial.unittest import TestCase

from towncrier import __version__
from towncrier._shell import towncrier


class TestCli(TestCase):
    def test_version(self):
        """
        The top level `--version` arguments returns towncrier own version.
        """

        runner = CliRunner()

        result = runner.invoke(towncrier, ["--version"])

        self.assertEqual(0, result.exit_code)
        self.assertEqual(result.output.strip(), f"towncrier, version {__version__}")
