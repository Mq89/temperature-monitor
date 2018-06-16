#!/usr/bin/env python
#-*- coding:utf-8 -*-

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
        self._log.info("attached observer " + str(obs))
        if not obs in self._observers:
            self._observers.append(obs)

    def stop(self):
        for obs in self._observers:
            obs.stop()
        self._run = False
        self._log.info("{0} stopped".format(self))
    
    def _notify(self, tin, tout):
        for obs in self._observers:
            obs.update(self, tin, tout)
    
    def getTemperature(self, dev = 0):
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
        try:
            while(self._run):
                start = datetime.now()
                tin = self.getTemperature(0)
                tout = self.getTemperature(1)
                self._notify(tin, tout)
                wait = int(self._intervall - (datetime.now() - start).total_seconds())
                while wait > 0 and self._run:
                    self._log.debug("wait = {}".format(wait))
                    time.sleep(1)
                    wait -= 1
            self._log.info("left control loop")
        except KeyboardInterrupt:
            self._log.info("Keyboard interrupt")
            pass

    def __str__(self):
        return self.__class__.__name__