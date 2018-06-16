#!/usr/bin/env python
#-*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
from threading import Thread
import logging

class SegPlugin:

    _SEGMENTS = (3,5,7,11,13,15,19)
    _DIGITS = (8,10,12,16)
    _NUM = {
        '-':(1,1,1,1,1,1,0),
        ' ':(1,1,1,1,1,1,1),
        '0':(0,0,0,0,0,0,1),
        '1':(1,0,0,1,1,1,1),
        '2':(0,0,1,0,0,1,0),
        '3':(0,0,0,0,1,1,0),
        '4':(1,0,0,1,1,0,0),
        '5':(0,1,0,0,1,0,0),
        '6':(0,1,0,0,0,0,0),
        '7':(0,0,0,1,1,1,1),
        '8':(0,0,0,0,0,0,0),
        '9':(0,0,0,0,1,0,0)
    }
    _DP = 21

    _LED = 22   # indicating outside temperature
    _LED2 = 24  # indicating inside temperature
    _LED3 = 23  # warning indicator (outside warmer than inside, outside below 0 degrees)

    def __init__(self):
        """ Initialisieren """
        self._log = logging.getLogger(str(self))
        self._log.info("{0} init".format(self))

        self._tin = 0
        self._tout = 0

        self._run = True
        self._initGPIO()
        self._formatValue(20)

        self._t1 = Thread(target=self._alternate)
        self._t1.start()

        self._t2 = Thread(target=self._runGPIO)
        self._t2.start()

    def _initGPIO(self):
        """ Raspberry GPIO initialisieren """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self._DIGITS, GPIO.OUT)
        GPIO.setup(self._SEGMENTS, GPIO.OUT)
        GPIO.setup(self._DP, GPIO.OUT)
        GPIO.setup(self._LED, GPIO.OUT)
        GPIO.setup(self._LED2, GPIO.OUT)
        GPIO.setup(self._LED3, GPIO.OUT)

        GPIO.output(self._DIGITS, 1)
        GPIO.output(self._SEGMENTS, 1)
        GPIO.output(self._DP, 0)
        GPIO.output(self._LED, 1)
        GPIO.output(self._LED2, 1)
        GPIO.output(self._LED3, 1)


    def update(self, mod, tin, tout):
        """ Werte aktualisieren """
        # print "update({0}, {1}, {2})".format(mod, tin, tout)
        self._tin = tin
        self._tout = tout

        # schalte LED2 ein, wenn draußen wärmer als drinnen, oder wenn draußen kälter als 0°C
        if (tin < tout or tout < 0):
            GPIO.output(self._LED2, 1)
        else:
            GPIO.output(self._LED2, 0)

    def stop(self):
        self._run = False
        self._log.info("{0} stopped".format(self))

    def _runGPIO(self):
        """ GPIO Schleife """
        while self._run:
            for digit in range(4):
                GPIO.output(self._SEGMENTS, self._NUM[self._value[digit]])
                GPIO.output(self._DIGITS[digit], 1)
                if digit == 2:
                    GPIO.output(self._DP, 0)
                else:
                    GPIO.output(self._DP, 1)
                time.sleep(0.001)
                GPIO.output(self._DIGITS[digit], 0)

    def _alternate(self):
        """ Wechsle zwischen innen und außen """
        wait = 3.0
        while self._run:

	    # inside
            t = int(time.strftime("%H"))
            self._value = self._formatValue(self._tin)
            GPIO.output(self._LED, 0)
            if 6 <= t < 22:
                GPIO.output(self._LED3, 1)
            time.sleep(wait)

	    # outside
            self._value = self._formatValue(self._tout)
            if 6 <= t < 22:
                GPIO.output(self._LED, 1)
            GPIO.output(self._LED3, 0)
            time.sleep(wait)

    def _formatValue(self, value):
        """ Wert für 7 Segment formatieren """
        if abs(value) >= 100:
            #self._log.error("formatValue(): value was out of range: {0}".format(value))
            return "----"
        if value < 0:
            newValue = "-"
        else:
            newValue = " "
        newValue += '{:4.1f}'.format(abs(value))
        return newValue.replace(".", "")

    def __str__(self):
        return self.__class__.__name__

    def __del__(self):
        self._log.info("GPIO.cleanup(). save to restart now.")
        GPIO.cleanup()

def main():
    t = SegPlugin()
    t.update(None, 20.0, -100)
    n = -20
    while True:
        try:
            time.sleep(1)
            n += 1
            t.update(None, n/10.0, -101)
            # pass
        except KeyboardInterrupt:
            t.stop()
            break

if __name__ == '__main__':
    main()
