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
# Filename: area.py
# 
# File Description: File dealing with areas


import os
import re
import glob

import olc
import room
import event
import world
import player
import mobile


arealist = []
roomlist = {}
mobilelist = {}
objectlist = {}

def init():
    areas = glob.glob(os.path.join(world.areaDir, '*'))
    for areapath in areas:
        newarea = oneArea(areapath)

def roomByVnum(vnum):
    if vnum in roomlist.keys():
        return roomlist[vnum]
    else:
        return False

_headerRe = re.compile(r'Header(.*?)ENDHeader', re.I | re.S)
_roomsRe = re.compile(r'Rooms(.*?)ENDRooms', re.I | re.S)
_mobsRe = re.compile(r'Mobs(.*?)ENDMobs', re.I | re.S)
_objectsRe = re.compile(r'Objects(.*?)ENDObjects', re.I | re.S)
_resetsRe = re.compile(r'Resets(.*?)ENDResets', re.I | re.S)
_shopsRe = re.compile(r'Shops(.*?)ENDShops', re.I | re.S)

planes = ('material',)

difficulty = ('all', 'very easy', 'easy', 'moderate', 'hard', 'very hard', 'extreme')

class oneArea(olc.Editable):
    def __init__(self, path):
        olc.Editable.__init__(self)
        self.path = path
        self.name = ''
        self.author = ''
        self.plane = ''
        self.hometown = ''
        self.difficulty = ''
        self.alignment = ''
        self.locationx = 0
        self.locationy = 0
        self.vnumlow = -1
        self.vnumhigh = -1
        self.roomlist = {}
        self.moblist = {}
        self.objectlist = {}
        self.mobindexlist = {}
        self.objectindexlist = {}
        self.resetlist = []
        self.shoplist = []
        self.playerlist = []
        self.events = []
        event.init_events_area(self)
        self.commands = {'name': ('string', None),
                         'author': ('string', None),
                         'plane': ('string', planes),
                         'hometown': ('string', None),
                         'difficulty': ('string', difficulty),
                         'alignment': ('string', None),
                         'locationx': ('integer', None),
                         'locationy': ('integer', None),
                         'vnumlow': ('integer', None),
                         'vnumhigh': ('integer', None)}
        if os.path.exists(self.path):
            self.load()

    def savedata(self):
        retdata = "name | {0}~\n"\
                  "author | {1}~\n"\
                  "plane | {2}~\n"\
                  "hometown | {3}~\n"\
                  "difficulty | {4}~\n"\
                  "alignment | {5}~\n"\
                  "locationx | {6}~\n"\
                  "locationy | {7}~\n"\
                  "vnum low | {8}~\n"\
                  "vnum high | {9}~\n".format(
                     self.name, self.author, self.plane, self.hometown, 
                     self.difficulty, self.alignment, self.locationx,
                     self.locationy, self.vnumlow, self.vnumhigh)
        return retdata

    def loaddata(self, data):
        data = [item.strip() for item in data if item.strip() != '']
        dictinfo = {}
        for thing in data:
            first = thing.index('|')
            dictinfo[thing[:first].strip()] = thing[first + 1:].strip()
        self.name = dictinfo['name']
        self.author = dictinfo['author']
        self.plane = dictinfo['plane']
        self.hometown = dictinfo['hometown']
        self.difficulty = dictinfo['difficulty']
        self.alignment = dictinfo['alignment']
        self.locationx = int(dictinfo['locationx'])
        self.locationy = int(dictinfo['locationy'])
        self.vnumlow = int(dictinfo['vnum low'])
        self.vnumhigh = int(dictinfo['vnum high'])

    def save(self):
        with open(self.path, 'w') as thefile:
            thefile.write('Header\n')
            thefile.write(self.savedata())
            thefile.write('ENDHeader\n\n')
            thefile.write('Rooms\n')
            for room in self.roomlist.keys():
                thefile.write(self.roomlist[room].savedata())
                thefile.write('$\n')
            thefile.write('ENDRooms\n\n')
            thefile.write('Mobs\n')
            if len(self.moblist) > 0:
                for mob in self.moblist:
                    thefile.write(mob.savedata())
                    thefile.write('$\n')
            thefile.write('ENDMobs\n\n')
            thefile.write('Objects\n')
            if len(self.objectlist) > 0:
                for oneobject in self.objectlist:
                    thefile.write(oneobject.savedata())
                    thefile.write('$\n')
            thefile.write('ENDObjects\n\n')
            thefile.write('Resets\n')
            if len(self.resetlist):
                for reset in self.resetlist:
                    thefile.write(reset.savedata())
                    thefile.write('$\n')
            thefile.write('ENDResets\n\n')
            thefile.write('Shops\n')
            if len(self.shoplist) > 0:
                for shop in self.shoplist:
                    thefile.write(shop.savedata())
                    thefile.write('$\n')
            thefile.write('ENDShops\n\n')

    def load(self):
        with open(self.path, 'r') as thefile:
            data = thefile.read()
        
        headmatch = _headerRe.search(data)
        if headmatch is not None:
            self.loaddata(headmatch.group(1).split('~'))
        else:
            print("Error matching header in {0}!".format(self.path))
        roomsmatch = _roomsRe.search(data)
        if roomsmatch is not None:
            roomlist = [item.strip() for item in
                        roomsmatch.group(1).split('$') if item.strip() != '']
            for eachroom in roomlist:
                room.oneRoom(self, eachroom)
        else:
            print("Error matching rooms in {0}!".format(self.path))
        mobsmatch = _mobsRe.search(data)
        if mobsmatch is not None:
            moblist = [item.strip() for item in
                       mobsmatch.group(1).split('$') if item.strip() != '']
            for mob in moblist:
                pass
        else:
            print("Error matching mobs in {0}!".format(self.path))
        objsmatch = _objectsRe.search(data)
        if objsmatch is not None:
            objectlist = [item.strip() for item in
                          objsmatch.group(1).split('$') if item.strip() != '']
            for object in objectlist:
                pass
        else:
            print("Error matching objects in {0}!".format(self.path))
        resetsmatch = _resetsRe.search(data)
        if resetsmatch is not None:
            resetlist = [item.strip() for item in
                         resetsmatch.group(1).split('$') if item.strip() != '']
            for reset in resetlist:
                pass
        else:
            print("Error matching resets in {0}!".format(self.path))
        shopsmatch = _shopsRe.search(data)
        if shopsmatch is not None:
            shoplist = [item.strip() for item in
                        shopsmatch.group(1).split('$') if item.strip() != '']
            for shop in shoplist:
                pass
        else:
            print("Error matching shoplist in {0}!".format(self.path))
        arealist.append(self)
        
    def display(self):
        retvalue = "{{WName{{x: {0}\n"\
                   "{{WAuthor{{x: {1}\n"\
                   "{{WPlane{{x: {2}\n"\
                   "{{WHometown{{x: {3}\n"\
                   "{{WDifficulty{{x: {4}\n"\
                   "{{WAlignment{{x: {5}\n"\
                   "{{WLocation X{{x: {6}\n"\
                   "{{WLocation Y{{x: {7}\n"\
                   "{{WVnum Low{{x: {8}\n"\
                   "{{WVnum High{{x: {9}\n".format(
                      self.name, self.author, self.plane, self.hometown,
                      self.difficulty, self.alignment, self.locationx,
                      self.locationy, self.vnumlow, self.vnumhigh)
        return retvalue