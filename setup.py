#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

from setuptools import setup, find_packages

# If incremental is not present then setuptools just silently uses v0.0.0 so
# let's import it and fail instead.
import incremental


setup(
    name="towncrier",
    maintainer="Amber Brown",
    maintainer_email="hawkowl@twistedmatrix.com",
    url="https://github.com/hawkowl/towncrier",
    project_urls={
        "Chat": "https://webchat.freenode.net/?channels=%23twisted",
        "Maillist": "https://twistedmatrix.com/cgi-bin/mailman/listinfo/twisted-python",
        "Issues": "https://github.com/twisted/towncrier/issues",
        "Repository": "https://github.com/twisted/towncrier",
        "Tests": "https://github.com/twisted/towncrier/actions?query=branch%3Amaster",
        "Coverage": "https://codecov.io/gh/twisted/towncrier",
        "Distribution": "https://pypi.org/project/towncrier",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    use_incremental=True,
    install_requires=[
        "click",
        "click-default-group",
        "incremental",
        "jinja2",
        "setuptools",
        "toml; python_version < '3.6'",
        "tomli; python_version >= '3.6'",
    ],
    extras_require={"dev": ["packaging"]},
    package_dir={"": "src"},
    packages=find_packages("src"),
    license="MIT",
    zip_safe=False,
    include_package_data=True,
    description="Building newsfiles for your project.",
    long_description=open("README.rst").read(),
    entry_points={"console_scripts": ["towncrier = towncrier._shell:cli"]},
)
