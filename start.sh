#!/bin/bash

cd /home/pi/temperature/

if ! [ -e pid ]; then
    ./main.py &
    echo $! > pid
else
    echo "Pidfile exists. Nothing to do..."
fi
