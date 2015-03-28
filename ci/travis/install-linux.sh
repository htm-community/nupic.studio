#!/bin/bash

echo
echo Running install-linux.sh...
echo

# Install NuPIC Studio
cd ${TRAVIS_BUILD_DIR}
sudo python setup.py install
