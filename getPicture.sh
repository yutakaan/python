#!/bin/bash
#

export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1

python3 $HOME/python/getPicture.py

exit 0

