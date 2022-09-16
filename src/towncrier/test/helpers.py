from functools import wraps
from pathlib import Path

from click.testing import CliRunner


def read(filename):
    return Path(filename).read_text()


def write(path, contents):
    """
    Create a file with given contents including any missing parent directories
    """
    p = Path(path)
    p.parent.mkdir(parents=True)
    p.write_text(contents)


def with_isolated_runner(fn):
    """
    Run *fn* within an isolated filesystem and add the kwarg *runner* to its
    arguments.
    """

    @wraps(fn)
    def test(*args, **kw):
        runner = CliRunner()
        with runner.isolated_filesystem():
            return fn(*args, runner=runner, **kw)

    return test


def setup_simple_project(
    *, config=None, pyproject_path="pyproject.toml", mkdir_newsfragments=True
):
    if config is None:
        config = "[tool.towncrier]\n" 'package = "foo"\n'

    Path(pyproject_path).write_text(config)
    Path("foo").mkdir()
    Path("foo/__init__.py").write_text('__version__ = "1.2.3"\n')

    if mkdir_newsfragments:
        Path("foo/newsfragments").mkdir()
