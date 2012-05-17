#! usr/bin/env python
# 
#  APM - Another Python Mud
#  Copyright (C) 2012  bdubyapee (BWP)
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
# Filename: room.py
# 
# File Description: Module dealing with rooms specifically.


import olc
import area
from fileparser import flatFileParse, listWrite, listRead, textRead
from fileparser import dictWrite, dictRead, boolRead, boolWrite
import event
import exits

flags = ('none', 'fire', 'dead zone', 'dark', 'sanctuary', 'peace', 'inn', 'nomagic')

sectortypes = ('inside', 'city', 'field', 'forest', 'hills', 'mountain', 'water',
               'deep water', 'air', 'desert', 'jungle', 'swamp', 'cave', 'underwater')

propertyvalues = ('very poor', 'poor', 'moderate', 'upper moderate', 'rich', 'very rich')

class oneRoom(olc.Editable):
    def __init__(self, area, data=None, vnum=None):
        olc.Editable.__init__(self)
        self.area = area
        self.builder = None
        if vnum != None:
            self.vnum = vnum
        else:
            self.vnum = 0
        self.name = 'Blank Room'
        self.description = ''
        self.propertyvalue = ''
        self.flags = []
        self.sectortype = []
        self.extradescriptions = {}
        self.exits = {}
        self.contents = []
        self.events = []
        event.init_events_room(self)
        self.commands = {'builder': ('string', None),
                         'vnum': ('integer', None),
                         'name': ('string', None),
                         'description': ('description', None),
                         'propertyvalue': ('string', propertyvalues),
                         'flags': ('list', flags),
                         'sectortype': ('list', sectortypes),
                         'extradescriptions': ('dict', (None, None))}
        if data is not None:
            self.load(data)

    def savedata(self):
        exitdata = {}
        for anexit in self.exits.keys():
            testoutput = self.exits[anexit].savedata()
            exitdata[str(anexit)] = testoutput
        retvalue = "vnum | {0}~\n"\
                   "name | {1}~\n"\
                   "description | {2}~\n"\
                   "exits | {3}~\n"\
                   "flags | {4}~\n"\
                   "sector type | {5}~\n"\
                   "property value | {6}~\n"\
                   "extra descriptions | {7}~\n".format(
                      self.vnum, self.name, self.description,
                      dictWrite(exitdata),
                      listWrite(self.flags),
                      listWrite(self.sectortype),
                      self.propertyvalue,
                      dictWrite(self.extradescriptions))
        return retvalue

    def load(self, data):
        data = data.split('~')
        data = [item.strip() for item in data if item.strip() != '']
        dictinfo = {}
        for thing in data:
            first = thing.index('|')
            dictinfo[thing[:first].strip()] = thing[first + 1:].strip()
        self.vnum = dictinfo['vnum']
        self.vnum = int(self.vnum)
        self.area.roomlist[self.vnum] = self
        area.roomlist[self.vnum] = self
        self.name = dictinfo['name']
        self.description = dictinfo['description']
        exitdata = dictRead(dictinfo['exits'])
        for oneexit in list(exitdata.keys()):
            self.exits[oneexit] = exits.Exit(self, ' '.join([oneexit, exitdata[oneexit]]))
        self.flags = listRead(dictinfo['flags'])
        self.sectortype = listRead(dictinfo['sector type'])
        self.propertyvalue = dictinfo['property value']
        self.extradescriptions = dictRead(dictinfo['extra descriptions'])

    def display(self):
        retvalue = "{{WArea{{x: {0}\n"\
                   "{{WBuilder{{x: {1}\n"\
                   "{{WVnum{{x: {2}\n"\
                   "{{WName{{x: {3}\n"\
                   "{{WDescription{{x: {4}\n"\
                   "{{WProperty Value{{x: {5}\n"\
                   "{{WFlags{{x: {6}\n"\
                   "{{WSector Type{{x: {7}\n"\
                   "{{WExtra Desc{{x: {8}\n"\
                   "{{WExits{{x: {9}\n".format(
                      self.area.name, self.builder.name, self.vnum, self.name,
                      self.description, self.propertyvalue, self.flags,
                      self.sectortype, self.extradescriptions, 
                      ', '.join(self.exits.keys()))
        return retvalue