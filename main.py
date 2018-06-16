#!/usr/bin/env python
#-*- coding:utf-8 -*-

import temperature
from plugins import sql_writer
from plugins import display
import logging
import logging.config
import signal
import time

def main():
    # logging.basicConfig(filename="temperature.log", level=logging.INFO, format='%(asctime)-15s %(name)-15s: %(message)s')
    logging.config.fileConfig('logging.conf')
    log = logging.getLogger("Main")
    log.info("###### NEW INSTANCE #####")
    log.log(51, "Current level is: {0}".format(logging.getLevelName(log.getEffectiveLevel())))
    t = temperature.Temperature()
    t.start()
    # t.attach(console.Console())
    t.attach(sql_writer.SQLWriter())
    t.attach(display.SegPlugin())
    # t.attach(notify.TempNotify())

    killer = GracefulKiller(t)
    while killer.getRun():
        time.sleep(1)
    log.info("left main method")

class GracefulKiller:
    def __init__(self, thread):
        self._thread = thread
        self._run = True
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def _exit_gracefully(self, signum, frame):
        logging.getLogger(str(self)).info("received SIGTERM")
        if not self._thread == None:
            self._thread.stop()
        self._run = False

    def getRun(self):
        return self._run

    def __str__(self):
        return self.__class__.__name__

if __name__ == '__main__':
    main()

