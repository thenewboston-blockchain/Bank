#!/bin/sh

find requirements/ -name '*.txt' -type f -delete
pip-compile -v -o requirements/base.txt requirements/base.in
pip-compile -v -o requirements/development.txt requirements/development.in
pip-compile -v -o requirements/local.txt requirements/local.in
pip-compile -v -o requirements/production.txt requirements/production.in
pip-compile -v -o requirements/staging.txt requirements/staging.in
