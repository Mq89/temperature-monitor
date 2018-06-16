#!/usr/bin/env python
#-*- coding:utf-8 -*-

import MySQLdb
import pylab
import matplotlib
import datetime
import time


while (True):
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        conn = MySQLdb.connect("nurthack", "temperature", "", "sensors")
        c = conn.cursor()
        c.execute("SELECT time, tin, tout FROM temperature WHERE time > '{0} 00:00:00'".format(today))

        x = []
        data = [[], []]
        for col in c.fetchall():
            x.append(col[0])
            data[0].append(col[1])
            data[1].append(col[2])

        conn.close()

        avg_in = sum(data[0])/len(data[0])
        avg_out = sum(data[1])/len(data[1])

        avg_in_v = [data[0][0]]
        avg_out_v = [data[1][0]]
        for i in range(1, len(x)):
            avg_in_v.append(sum(data[0][0:i+1]) / (i+1))
            avg_out_v.append(sum(data[1][0:i+1]) / (i+1))

        t = 3
        mavg_in = []
        mavg_out = []
        for i in range(len(x)):
            a = i - t/2
            b = i + t/2 + 1
            if (a < 0):
                a = 0
            d = data[0][a:b]
            mavg_in.append(sum(d) / len(d))
            d = data[1][a:b]
            mavg_out.append(sum(d) / len(d))

        pylab.figure()
        pylab.title("Temperatur {0}".format(datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y")))
        pylab.xlabel("Zeit")
        pylab.ylabel(u"Temperatur [°C]")

        pylab.plot([x[0], x[-1]], [avg_in, avg_in], color=(0,0,1,.4))
        pylab.plot([x[0], x[-1]], [avg_out, avg_out], color=(1,0,0,.4))
        pylab.plot([x[0], x[-1]], [mavg_in[-1], mavg_in[-1]], '-.', color=(0,0,1,.8))
        pylab.plot([x[0], x[-1]], [mavg_out[-1], mavg_out[-1]], '-.', color=(1,0,0,.8))
        pylab.plot(x, data[0], ':', color=(0,0,1,.4))
        pylab.plot(x, data[1], ':', color=(1,0,0,.4))
        pylab.plot(x, avg_in_v, '--', color=(0,0,1,.3))
        pylab.plot(x, avg_out_v, '--', color=(1,0,0,.3))
        pylab.plot(x, mavg_in, 'b-', label=u"innen")
        pylab.plot(x, mavg_out, 'r-', label=u"außen")

        pylab.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
        pylab.legend()
        pylab.grid(True)
        pylab.show()
    except KeyboardInterrupt:
        break







