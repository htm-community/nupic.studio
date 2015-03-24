#!/bin/bash

echo
echo Running install-linux.sh...
echo

# Verify python version
python --version

# Install NuPIC Studio
cd ${TRAVIS_BUILD_DIR}
python setup.py install --user
