#!/usr/bin/env python
#-*- coding:utf-8 -*-

from gi.repository import Notify
from datetime import datetime
import temperature as t
import logging

class TempNotify:
    def __init__(self):
        Notify.init("Temperatur")
        self._notify("Temperature measurement started.")
        self._tin_old = None
        self._tout_old = None
        self._max_diff = 0
        self._log = logging.getLogger(str(self))
        self._log.info("libnotify plugin started")
        self._notify_difference = 2

    def update(self, mod, tin, tout):
        if (self._tin_old == None or self._tout_old == None):
            self._tin_old = tin
            self._tout_old = tout
            return

        tin_old = self._tin_old
        tout_old = self._tout_old

        diff_old = tout_old - tin_old
        diff = tout - tin
        self._max_diff = max(self._max_diff, abs(diff))
        self._log.info("maxdiff = " + str(self._max_diff))

        time = datetime.now().strftime("%H:%M")
        if tin > t.Temperature.MIN_VALUE and tout > t.Temperature.MIN_VALUE:
            # drinnen vs. draußen
            if (diff_old < 0 and diff >= 0) or (diff_old > 0 and diff <= 0):
                if self._max_diff >= self._notify_difference:
                    if (diff_old < 0 and diff >= 0):
                        self._notify("{2}:\n Es ist jetzt draußen ({1:.1f} °C)\nwärmer als drinnen ({0:.1f} °C).".format(tin, tout, time))
                        self._log.info("Notified warmer.")

                    if (diff_old > 0 and diff <= 0):
                        self._notify("{2}:\n Es ist jetzt draußen ({1:.1f} °C)\nkälter als drinnen ({0:.1f} °C).".format(tin, tout, time))
                        self._log.info("Notified colder.")
                else:
                    self._log.info("Ratio change. Notification omitted as difference was not > " + str(self._notify_difference))

                self._max_diff = 0


            # Gefrierpunkt
            if (tout_old < 0 and tout >= 0):
                self._notify("{0}:\n Die Außentemperatur liegt jetzt über dem Gefrierpunkt".format(time))

            if (tout_old > 0 and tout <= 0):
                self._notify("{0}:\n Die Außentemperatur liegt jetzt unter dem Gefrierpunkt".format(time))
        else:
            self._notify("Lesefehler!")

        self._tin_old = tin
        self._tout_old = tout

    def _notify(self, msg):
        n = Notify.Notification.new("Temperatur", msg, "dialog-information")
        n.show()

    def __str__(self):
        return self.__class__.__name__
