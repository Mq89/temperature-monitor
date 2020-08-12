#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from lib import temper
import time
import threading
import usb.core
from datetime import datetime


class Temperature(threading.Thread):

    MIN_VALUE = -273.15

    def __init__(self):
        threading.Thread.__init__(self)
        self._log = logging.getLogger(str(self))
        self._log.info("{0} init".format(self))

        self._observers = []
        self._temper = temper.TemperHandler()
        self._intervall = 60
        self._run = True

    def attach(self, obs):
        """
        @brief      Attach a observer

        @param      self  The object
        @param      obs   The observer to attach

        @return     None
        """
        self._log.info("attached observer " + str(obs))
        if obs not in self._observers:
            self._observers.append(obs)

    def stop(self):
        """
        @brief      Stop this class and all observers.

        @param      self  The object

        @return     None
        """
        for obs in self._observers:
            obs.stop()
        self._run = False
        self._log.info("{0} stopped".format(self))

    def _notify(self, tin, tout):
        """
        @brief      Update all observers with new temperature values.

        @param      self  The object
        @param      tin   The new inside temperature
        @param      tout  The new outside temperature

        @return     None
        """
        for obs in self._observers:
            obs.update(self, tin, tout)

    def getTemperature(self, dev=0):
        """
        @brief      Read the temperature from a device.

        @param      self  The object
        @param      dev   The device to read the temperature value from.

        @return     A float greater or equal than self.MIN_VALUE.
        """
        self._log.debug("getTemperature({})".format(dev))
        devices = self._temper.get_devices()
        if len(devices) < dev:
            self._log.error("Tried to get temperature from device " + str(dev) + " that is not available.")
            return Temperature.MIN_VALUE
        try:
            return devices[dev].get_temperature()
        except usb.core.USBError as e:
            self._log.error(e)
            return Temperature.MIN_VALUE

    def run(self):
        """
        @brief      Control logic, reading the temperature values every
                    self._intervall seconds

        @param      self  The object

        @return     { description_of_the_return_value }
        """
        try:

            # control loop
            while(self._run):

                if int(time.time()) % self._intervall == 0:

                    # read values
                    tin = self.getTemperature(0)
                    tout = self.getTemperature(1)

                    # update all attached plugins
                    self._notify(tin, tout)

                    # ensure that we end up in the next second
                    time.sleep(1)

                # wait a bit less than a second to accommodate for
                # the execution time of the loop
                time.sleep(.99)

            self._log.info("left control loop")
        except KeyboardInterrupt:
            self._log.info("Keyboard interrupt")
            pass

    def __str__(self):
        return self.__class__.__name__
