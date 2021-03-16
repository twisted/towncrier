#!/usr/bin/bash

set -e

twine check {toxinidir}/dist/*
