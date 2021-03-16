#!/usr/bin/bash

set -evx

twine check {toxinidir}/dist/*
