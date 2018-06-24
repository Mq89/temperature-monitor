#!/bin/bash

# the pidfile
PIDFILE="/home/pi/temperature/pid"

# check if pidfile exists and send SIGTERM to the corresponding process
if [ -e $PIDFILE ]
	then
	kill $(< $PIDFILE)
	rm $PIDFILE

    # wait for GPIO.cleanup() to be executed to allow a clean stop
	echo "GPIO.cleanup() abwarten!"
fi
