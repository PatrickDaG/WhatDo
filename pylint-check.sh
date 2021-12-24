#!/bin/bash
pylint src/autokernel --ignore=version.py --disable=line-too-long,invalid-name,too-many-instance-attributes,too-few-public-methods,too-many-arguments,too-many-locals,duplicate-code"${1:+,}$1"
mypy src/autokernel
