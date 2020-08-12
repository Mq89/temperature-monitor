#!/usr/bin/env python
# -*- coding:utf-8 -*-

import temperature
from plugins import sql_writer
from plugins import display
import logging
import logging.config
import signal
import time

def main():

    # set up logging
    logging.config.fileConfig('logging.conf')
    log = logging.getLogger("Main")
    log.info("###### NEW INSTANCE #####")
    log.log(51, "Current level is: {0}".format(logging.getLevelName(log.getEffectiveLevel())))

    # start the main class
    t = temperature.Temperature()
    t.start()

    # attach observers
    # t.attach(console.Console())
    t.attach(sql_writer.SQLWriter())
    t.attach(display.SegPlugin())
    # t.attach(notify.TempNotify())

    # start object catching SIGTERM
    killer = GracefulKiller(t)
    while killer.getRun():
        time.sleep(1)
    log.info("left main method")


class GracefulKiller:
    """
    @brief      Class to catch SIGTERM and stop an enclosed thread.
    """

    def __init__(self, thread):
        """
        @brief      Constructs the object.

        @param      self    The object
        @param      thread  The thread to stop, after catching SIGTERM
        """
        self._thread = thread
        self._run = True

        # register to catch SIGTERM
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def _exit_gracefully(self, signum, frame):
        """
        @brief      Method to catch SIGTERM

        @param      self    The object
        @param      signum  The signum
        @param      frame   The frame

        @return     None
        """
        logging.getLogger(str(self)).info("received SIGTERM")
        if self._thread is not None:
            # stop the enclosed thread
            self._thread.stop()
        self._run = False

    def getRun(self):
        """
        @brief      Returns true as long as no SIGTERM has been catched.

        @param      self  The object

        @return     Boolean. True as long as no SIGTERM has been catched.
        """
        return self._run

    def __str__(self):
        return self.__class__.__name__


if __name__ == '__main__':
    main()
