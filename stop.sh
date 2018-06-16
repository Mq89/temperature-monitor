#!/bin/bash
PIDFILE="/home/pi/temperature/pid"

if [ -e $PIDFILE ]
	then
	kill $(< $PIDFILE)
	rm $PIDFILE
	echo "GPIO.cleanup() abwarten!"
fi
