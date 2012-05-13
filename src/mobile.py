#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: mobile.py
# 
# File Description: Eventually the home of the mobiles.
# 
# By: admin

import event
import livingthing

class Mobile(livingthing.LivingThing):
    def __init__(self):
        livingthing.LivingThing.__init__(self)
        self.ismobile = True
        self.keywords = []
        self.events = []
        event.init_events_mobile(self)
        
    def savedata(self):
        pass
    
    def loaddata(self):
        pass
