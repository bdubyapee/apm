#! usr/bin/env python
# 
#  APM - Another Python Mud
#  Copyright (C) 2012  bdubyapee (BWP) p h i p p s b @ g m a i l . c o m
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Filename: mobile.py
# 
# File Description: Eventually the home of the mobiles.


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
