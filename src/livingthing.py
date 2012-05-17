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
# Filename: livingthing.py
# 
# File Description: The livingthing module.  All living things inherit from this.
#                   This includes mobiles and players.


import races
import comm


# Module variables here

positions = ('sleeping', 'sitting', 'standing')
genders = ('male', 'female', 'other')
stat_types = ('strength', 'agility', 'speed', 'intelligence',
              'wisdom', 'charisma', 'luck', 'constitution')
disciplines = ('physical', 'mental', 'mystic', 'religious')

class LivingThing:
    def __init__(self):
        self.name = ''
        self.lastname = ''
        self.long_description = ''
        self.short_description = ''
        self.gender = 'male'
        self.location = None
        self.race = None
        self.age = 1
        self.level = 1
        self.alignment = 'neutral'
        self.maximum_stat = {'strength': 1, 'agility': 1, 'speed': 1, 'intelligence': 1,
                             'wisdom': 1, 'charisma': 1, 'luck': 1, 'constitution': 1}
        self.current_stat = {'strength': 1, 'agility': 1, 'speed': 1, 'intelligence': 1,
                             'wisdom': 1, 'charisma': 1, 'luck': 1, 'constitution': 1}
        self.money = {'copper': 0,
                      'silver': 0,
                      'gold': 0,
                      'platinum': 0}
        self.height = {'feet': 0,
                       'inches': 0}
        self.weight = 1
        self.maxhp = 1
        self.currenthp = 1
        self.maxmovement = 1
        self.currentmovement = 1
        self.maxwillpower = 0
        self.currentwillpower = 0
        self.hitroll = 0
        self.damroll = 0
        self.totalmemoryslots = {'first circle' : 0,
                                 'second circle' : 0,
                                 'third circle': 0,
                                 'fourth circle': 0,
                                 'fifth circle': 0,
                                 'sixth circle': 0,
                                 'seventh circle': 0,
                                 'eighth circle': 0,
                                 'ninth circle': 0}
        self.memorizedspells = {}
        self.guild = None
        self.council = None
        self.family = None
        self.clan = None
        self.deity = ''
        self.discipline = None
        self.inventory = []
        self.worn = {}
        self.baceac = {'slashing' : 0,
                       'piercing' : 0,
                       'bashing' : 0,
                       'lashing' : 0}
        self.currentac = {'slashing' : 0,
                          'piercing' : 0,
                          'bashing' : 0,
                          'lashing' : 0}
        self.position = None
        self.knownpeople = {}

    # Utility functions for living things.
    def move(self, tospot=None, fromspot=None):
        if tospot == None:
            comm.wiznet("Received None value in move:livingthing.py")
            return
        else:
            if fromspot != None:
                fromspot.contents.remove(self)
            tospot.contents.append(self)
            self.location = tospot
            
    def addKnown(self, idnum=None, name=None):
        if idnum == None or name == None:
            comm.wiznet("You must provide id and name arguments.  addKnown:livingthing.py")
            return
        else:
            self.knownpeople[idnum] = name

    def getKnown(self, idnum=None):
        if id == None:
            comm.wiznet("You must provide an ID to lookup. getKnown:livingthing.py")
            return
        elif idnum not in self.knownpeople.keys():
            return ''
        else:
            return self.knownpeople[idnum]
        
