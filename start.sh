#!/bin/bash

# make sure we are in the correct directory
cd /home/pi/temperature/

# check whether pidfile exists and start program
if ! [ -e pid ]; then
    ./main.py &
    echo $! > pid
else
    echo "Pidfile exists. Nothing to do..."
fi
