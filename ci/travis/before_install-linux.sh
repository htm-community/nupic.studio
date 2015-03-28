#!/bin/bash

echo
echo Running before_install-linux.sh...
echo

echo ">>> Preparing environment..."

# TODO: remove when Travis has gcc>=4.8, gcc-4.8 is used for C++11 compatibility
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo apt-get update -qq
sudo apt-get install -qq gcc-4.8 g++-4.8
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 90
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 90

# Install virtual display
sudo apt-get install xvfb

# Install NuPIC
sudo pip install https://s3-us-west-2.amazonaws.com/artifacts.numenta.org/numenta/nupic/releases/nupic-0.2.1-cp27-none-linux_x86_64.whl
