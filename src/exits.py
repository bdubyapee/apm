#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: room.py
# 
# File Description: Module dealing with rooms specifically.
# 
# By: admin

import olc
import area
import event

directions = ('north', 'south', 'east', 'west', 'northwest', 'northeast',
              'southwest', 'southeast', 'up', 'down')

exitsizes = ('huge', 'large', 'medium', 'tiny')

oppositedirection = {'north': 'south',
                     'south': 'north',
                     'east': 'west',
                     'west': 'east',
                     'northwest': 'southeast',
                     'northeast': 'southwest',
                     'southwest': 'northeast',
                     'southeast': 'northwest',
                     'up': 'down',
                     'down': 'up'}

class Exit(olc.Editable):
    def __init__(self, room, data=None):
        olc.Editable.__init__(self)
        self.room = room
        self.direction = ''
        self.destination = 0
        self.locked = 'false'
        self.lockdifficulty = 0
        self.keyvnum = 0
        self.magiclocked = 'false'
        self.physicaldiffuculty = 0
        self.magiclockdifficulty = 0
        self.casterid = 0
        self.magiclocktype = 'none'
        self.size = 'Huge'
        self.hasdoor = 'false'
        self.dooropen = 'true'
        self.keywords = []
        self.events = []
        event.init_events_exit(self)
        self.commands = {'direction': ('string', directions),
                         'destination': ('integer', None),
                         'locked': ('string', ['true', 'false']),
                         'lockdifficulty': ('integer', None),
                         'keyvnum': ('integer', None),
                         'magiclocked': ('string', ['true', 'false']),
                         'physicaldifficulty': ('integer', None),
                         'magiclockdifficulty': ('integer', None),
                         'casterid': ('integer', None),
                         'magiclocktype': ('string', None),
                         'size': ('string', exitsizes),
                         'hasdoor': ('string', ['true', 'false']),
                         'dooropen': ('string', ['true', 'false']),
                         'keywords': ('list', None)}
        if data is not None:
            self.load(data)

    def savedata(self):
        thelist = [str(self.destination),
                   self.locked,
                   str(self.lockdifficulty),
                   str(self.keyvnum),
                   self.magiclocked,
                   str(self.physicaldifficulty),
                   str(self.magiclockdifficulty),
                   str(self.casterid),
                   self.magiclocktype,
                   self.size,
                   self.hasdoor,
                   self.dooropen,
                   ', '.join(self.keywords)]
        output = ' '.join(thelist)
        return output

    def load(self, data):
        data = data.split()
        self.direction = data[0]
        self.destination = int(data[1])
        self.locked = data[2]
        self.lockdifficulty = int(data[3])
        self.keyvnum = int(data[4])
        self.magiclocked = data[5]
        self.physicaldifficulty = int(data[6])
        self.magiclockdifficulty = int(data[7])
        self.casterid = int(data[8])
        self.magiclocktype = data[9]
        self.size = data[10]
        self.hasdoor = data[11]
        self.dooropen = data[12]
        self.keywords = data[13:]

    def display(self):
        retvalue = "{{WRoom{{x: {0}\n"\
                   "{{WDirection{{x: {1}\n"\
                   "{{WDestination{{x: {2}\n"\
                   "{{WLocked{{x: {3}\n"\
                   "{{WLock Difficulty{{x: {4}\n"\
                   "{{WKey Vnum{{x: {5}\n"\
                   "{{WMagic Locked{{x: {6}\n"\
                   "{{WPhysical Difficulty{{x: {7}\n"\
                   "{{WMagic Lock Difficulty{{x: {8}\n"\
                   "{{WCaster ID{{x: {9}\n"\
                   "{{WMagic Lock Type{{x: {10}\n"\
                   "{{WSize{{x: {11}\n"\
                   "{{WHas Door{{x: {12}\n"\
                   "{{WDoor Open{{x: {13}\n"\
                   "{{WKeywords{{x: {14}\n".format(
                      self.room.name, self.direction, self.destination,
                      self.locked, self.lockdifficulty, self.keyvnum,
                      self.magiclocked, self.physicaldifficulty,
                      self.magiclockdifficulty, self.casterid, 
                      self.magiclocktype, self.size, self.hasdoor,
                      self.dooropen, self.keywords)
        return retvalue