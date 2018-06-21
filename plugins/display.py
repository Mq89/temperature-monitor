#!/usr/bin/env python
#-*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
from threading import Thread
import logging

class SegPlugin:

    # hours of day where the LED are allowed to be active
    _HOURS = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    # GPIO pins for the 7 segmets
    _SEGMENTS = (3,5,7,11,13,15,19)

    # GPIO to select the digits
    _DIGITS = (8,10,12,16)

    # which of the 7 segments should be switched on to display the character
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

    # GPIO pin for the dots between the digits
    _DP = 21

    _LED = 22   # indicating outside temperature
    _LED2 = 24  # indicating inside temperature
    _LED3 = 23  # warning indicator (outside warmer than inside, outside below 0 degrees)

    def __init__(self):
        """
        Initialize the class.
        
        @param      self  The object
        """
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
        """
        Initialize RPi GPIO.
        
        @param      self  The object
        
        @return     None
        """
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
        """
        @brief      Receive update of the temperature values.
        
        @param      self  The object
        @param      mod   The modifier
        @param      tin   The inside temperature value
        @param      tout  The outside temperature value
        
        @return     None
        """

        # print "update({0}, {1}, {2})".format(mod, tin, tout)
        self._tin = tin
        self._tout = tout

        # schalte LED2 ein, wenn draußen wärmer als drinnen, oder wenn draußen
        # kälter als 0°C
        if (tin < tout or tout < 0):
            GPIO.output(self._LED2, 1)
        else:
            GPIO.output(self._LED2, 0)

    def stop(self):
        """
        @brief      Stop the LED loop
        
        @param      self  The object
        
        @return     None
        """
        self._run = False
        self._log.info("{0} stopped".format(self))

    def _runGPIO(self):
        """
        @brief      The LED loop. Loops over all digit and switches the
                    repsective segments on to show the values safed in
                    self._value.
        
        @param      self  The object
        
        @return     None
        """
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
        """
        @brief      Alternate inside and outside temperature every 3 seconds
        
        @param      self  The object
        
        @return     None
        """

        wait = 3.0 # time to wait between switches
    
        while self._run:
	    # inside
            t = int(time.strftime("%H"))
            self._value = self._formatValue(self._tin)
            GPIO.output(self._LED, 0)
            if t in _HOURS:
                GPIO.output(self._LED3, 1)
            time.sleep(wait)

	    # outside
            self._value = self._formatValue(self._tout)
            if t in _HOURS:
                GPIO.output(self._LED, 1)
            GPIO.output(self._LED3, 0)
            time.sleep(wait)

    def _formatValue(self, value):
        """
        Format a temperature value for the 7 segment display.
        
        @param      self   The object
        @param      value  The value
        
        @return     The formatted value.
        """
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
        """
        @brief      Returns a string representation of the object.
        
        @param      self  The object
        
        @return     String representation of the object.
        """
        return self.__class__.__name__

    def __del__(self):
        self._log.info("GPIO.cleanup(). Save to restart now.")
        GPIO.cleanup()


def main():
    """
    @brief      Main method to test the plugin.
    
    @return     None
    """

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
