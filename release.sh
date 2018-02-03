#!/usr/bin/env bash

rm -Rf dist
./setup.py sdist
twine upload dist/*