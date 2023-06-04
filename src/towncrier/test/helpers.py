from __future__ import annotations

import sys
import textwrap

from functools import wraps
from pathlib import Path
from typing import Any, Callable

from click.testing import CliRunner


if sys.version_info < (3, 9):
    import importlib_resources as resources
else:
    from importlib import resources


def read(filename: str | Path) -> str:
    return Path(filename).read_text()


def write(path: str | Path, contents: str, dedent: bool = False) -> None:
    """
    Create a file with given contents including any missing parent directories
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if dedent:
        contents = textwrap.dedent(contents)
    p.write_text(contents)


def read_pkg_resource(path: str) -> str:
    """
    Read *path* from the towncrier package.
    """
    return (resources.files("towncrier") / path).read_text("utf8")


def with_isolated_runner(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Run *fn* within an isolated filesystem and add the kwarg *runner* to its
    arguments.
    """

    @wraps(fn)
    def test(*args: Any, **kw: Any) -> Any:
        runner = CliRunner()
        with runner.isolated_filesystem():
            return fn(*args, runner=runner, **kw)

    return test


def setup_simple_project(
    *,
    config: str | None = None,
    extra_config: str = "",
    pyproject_path: str = "pyproject.toml",
    mkdir_newsfragments: bool = True,
) -> None:
    if config is None:
        config = "[tool.towncrier]\n" 'package = "foo"\n' + extra_config

    Path(pyproject_path).write_text(config)
    Path("foo").mkdir()
    Path("foo/__init__.py").write_text('__version__ = "1.2.3"\n')

    if mkdir_newsfragments:
        Path("foo/newsfragments").mkdir()
