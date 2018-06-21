#!/usr/bin/env python
#-*- coding:utf-8 -*-

import MySQLdb
import logging
import temperature as t

class SQLWriter():
    def __init__(self):
        self._log = logging.getLogger(str(self))
        self._log.info("{0} init".format(self))

        self._user = "temperature"
        self._server = "nurthack"
        self._db = "sensors"
        self._tab = "data"  

    def update(self, mod, tin, tout):
        """
        @brief      Receive updates of temperature values
        
        @param      self  The object
        @param      mod   The modifier
        @param      tin   The inside temperature
        @param      tout  The outside temperature
        
        @return     None
        """

        # Insert query
        query = "INSERT INTO {0} (sensor_id, value) VALUES ({1}, {2})"

        try:
            connection = MySQLdb.connect(self._server, self._user, "", self._db)
            cursor = connection.cursor()

            # perform plausibility check on inside temperature and write into database
            if tin > t.Temperature.MIN_VALUE and tin < 100:
                cursor.execute(query.format(self._tab, 1, tin))
            else:
                self._log.error("tin out of range: {0}".format(tin))

            # perform plausibility check on outside temperature and write into database
            if tout > t.Temperature.MIN_VALUE and tout < 100:
                cursor.execute(query.format(self._tab, 2, tout))
            else:
                self._log.error("tout out of range: {0}".format(tout))
            connection.commit()
            connection.close()
        except MySQLdb.OperationalError as e:
            self._log.error("Connection Error: Values {0}, {1}".format(tin, tout))

    def stop(self):
        """
        @brief      Stop the plugin
        
        @param      self  The object
        
        @return     None
        """
        self._log.info("{0} stopped".format(self))

    def __str__(self):
        return self.__class__.__name__
