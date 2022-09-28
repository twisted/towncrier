#!/usr/bin/env python


# If incremental is not present then setuptools just silently uses v0.0.0 so
# let's import it and fail instead.
import incremental  # noqa

from setuptools import find_packages, setup


setup(
    name="towncrier",
    url="https://github.com/twisted/towncrier",
    project_urls={
        "Documentation": "https://towncrier.readthedocs.io/",
        "Chat": "https://web.libera.chat/?channels=%23twisted",
        "Mailing list": "https://mail.python.org/mailman3/lists/twisted.python.org/",
        "Issues": "https://github.com/twisted/towncrier/issues",
        "Repository": "https://github.com/twisted/towncrier",
        "Tests": "https://github.com/twisted/towncrier/actions?query=branch%3Atrunk",
        "Coverage": "https://codecov.io/gh/twisted/towncrier",
        "Distribution": "https://pypi.org/project/towncrier",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    use_incremental=True,
    python_requires=">=3.7",
    install_requires=[
        "click",
        "click-default-group",
        "incremental",
        "jinja2",
        "setuptools",
        "tomli; python_version<'3.11'",
    ],
    extras_require={
        "dev": [
            "packaging",
            "sphinx >= 5",
            "furo",
            "twisted",
        ],
    },
    package_dir={"": "src"},
    packages=find_packages("src"),
    license="MIT",
    zip_safe=False,
    include_package_data=True,
    description="Building newsfiles for your project.",
    long_description=open("README.rst").read(),
    entry_points={"console_scripts": ["towncrier = towncrier._shell:cli"]},
)
