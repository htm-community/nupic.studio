#!/bin/bash

echo
echo Running script-linux.sh...
echo

# Run NuPIC Studio from a virtual display
xvfb-run --server-args='-screen 0 640x480x16' nustudio
