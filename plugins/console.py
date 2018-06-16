#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime

class Console:
    def __init__(self):
        pass
    
    def update(self, mod, tin, tout):
        time = datetime.now().strftime("%H:%M:%S")
        print "{2} | In: {0:3.4f} Out: {1:3.4f}".format(tin, tout, time)
