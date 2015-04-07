#!/bin/bash

echo
echo Running before_install-osx.sh...
echo

echo ">>> Preparing environment..."

# Install NuPIC
sudo pip install nupic

# Install PyQt4
brew install pyqt
