#!/bin/bash

echo
echo Running before_install-linux.sh...
echo

echo ">>> Configuring environment..."
sudo add-apt-repository -y ppa:fkrull/deadsnakes
sudo apt-get update

# TODO: remove when Travis has gcc>=4.8
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo apt-get -qq update
sudo apt-get -qq install g++-4.8
alias gcc='gcc-4.8'        
alias g++='g++-4.8'

if [ $CC == 'gcc' ]; then
    export CC='gcc-4.8'
    export CXX='g++-4.8'
fi
