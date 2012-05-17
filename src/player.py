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
# Filename: player.py
# 
# File Description: The player module.


import os

import area
import livingthing
import room
from fileparser import flatFileParse, listWrite, listRead, textRead
from fileparser import dictWrite, dictRead, boolRead, boolWrite
import exits
import helpsys
import event
import races
import event
import world
import commands

playerlist = []
        
class Player(livingthing.LivingThing):
    def __init__(self, path=None):
        livingthing.LivingThing.__init__(self)
        self.filename = path
        self.logpath = ''
        self.isplayer = True
        self.capability = []
        self.password = ''
        self.lasthost = ''
        self.lasttime = ''
        self.wimpy = 0
        self.title = ''
        self.skillpoints = 0
        self.seen_as = ''
        self.aesthetic = ''
        self.aid = 0
        self.hunger = 0
        self.thirst = 0
        self.snooped_by = []
        self.prompt = ''
        self.alias = {}
        self.oocflags = {'afk': False,
                         'viewOLCdetails' : False,
                         'coding': False}
        self.exp = {'combat': 0,
                    'explore': 0,
                    'profession': 0}
        self.events = []
        event.init_events_player(self)
        self.sock = None
        if self.filename != None:
            self.load()

    def load(self):
        dictinfo = flatFileParse(self.filename)
        self.name = textRead(dictinfo['name'])
        self.password = textRead(dictinfo['password'])
        self.capability = listRead(dictinfo['capability'])
        self.lasthost = textRead(dictinfo['lasthost'])
        self.lasttime = textRead(dictinfo['lasttime'])
        newroom = int(textRead(dictinfo['location']))
        newroom = area.roomByVnum(newroom)
        self.location = newroom
        self.move(newroom)
        self.long_description = textRead(dictinfo['long description'])
        self.short_description = textRead(dictinfo['short description'])
        self.race = races.racebyname(textRead(dictinfo['race']))
        self.age = int(textRead(dictinfo['age']))
        self.gender = textRead(dictinfo['gender'])
        self.level = int(textRead(dictinfo['level']))
        self.alignment = textRead(dictinfo['alignment'])
        self.money = dictRead(dictinfo['money'])
        self.height = dictRead(dictinfo['height'])
        self.weight = int(textRead(dictinfo['weight']))
        self.maxhp = int(textRead(dictinfo['maxhp']))
        self.currenthp = int(textRead(dictinfo['currenthp']))
        self.maxmovement = int(textRead(dictinfo['maxmovement']))
        self.currentmovement = int(textRead(dictinfo['currentmovement']))
        self.maxwillpower = int(textRead(dictinfo['maxwillpower']))
        self.currentwillpower = int(textRead(dictinfo['currentwillpower']))
        self.totalmemoryslots = dictRead(dictinfo['totalmemoryslots'])
        self.memorizedspells = dictRead(dictinfo['memorizedspells'])
        self.hitroll = int(textRead(dictinfo['hitroll']))
        self.damroll = int(textRead(dictinfo['damroll']))
        self.wimpy = int(textRead(dictinfo['wimpy']))
        self.title = textRead(dictinfo['title'])
        self.guild = textRead(dictinfo['guild'])
        self.council = textRead(dictinfo['council'])
        self.family = textRead(dictinfo['family'])
        self.clan = textRead(dictinfo['clan'])
        self.deity = textRead(dictinfo['deity'])
        self.skillpoints = int(textRead(dictinfo['skillpoints']))
        self.seen_as = textRead(dictinfo['seen as'])
        self.maximum_stat = dictRead(dictinfo['maximum stat'])
        self.current_stat = dictRead(dictinfo['current stat'])
        self.discipline = textRead(dictinfo['discipline'])
        self.aesthetic = textRead(dictinfo['aesthetic'])
        self.exp = dictRead(dictinfo['exp'])
        self.inventory = listRead(dictinfo['inventory'])
        self.worn = dictRead(dictinfo['worn'])
        self.baceac = dictRead(dictinfo['baceac'])
        self.currentac = dictRead(dictinfo['currentac'])
        self.hunger = int(textRead(dictinfo['hunger']))
        self.thirst = int(textRead(dictinfo['thirst']))
        self.position = textRead(dictinfo['position'])
        self.aid = textRead(dictinfo['aid'])
        self.knownpeople = dictRead(dictinfo['known people'])
        self.prompt = textRead(dictinfo['prompt'])
        self.alias = dictRead(dictinfo['alias'])

    def save(self):
        with open(self.filename, 'w') as thefile:
            thefile.write('name | {0}~\n'.format(self.name))
            thefile.write('password | {0}~\n'.format(self.password))
            thefile.write('capability | {0}~\n'.format(listWrite(self.capability)))
            thefile.write('lasthost | {0}~\n'.format(self.lasthost))
            thefile.write('lasttime | {0}~\n'.format(self.lasttime))
            thefile.write('location | {0}~\n'.format(self.location.vnum))
            thefile.write('long description | {0}~\n'.format(self.long_description))
            thefile.write('short description | {0}~\n'.format(self.short_description))
            thefile.write('race | {0}~\n'.format(self.race.name))
            thefile.write('age | {0}~\n'.format(self.age))
            thefile.write('gender | {0}~\n'.format(self.gender))
            thefile.write('level | {0}~\n'.format(self.level))
            thefile.write('alignment | {0}~\n'.format(self.alignment))
            thefile.write('money | {0}~\n'.format(dictWrite(self.money)))
            thefile.write('height | {0}~\n'.format(dictWrite(self.height)))
            thefile.write('weight | {0}~\n'.format(self.weight))
            thefile.write('maxhp | {0}~\n'.format(self.maxhp))
            thefile.write('currenthp | {0}~\n'.format(self.currenthp))
            thefile.write('maxmovement | {0}~\n'.format(self.maxmovement))
            thefile.write('currentmovement | {0}~\n'.format(self.currentmovement))
            thefile.write('maxwillpower | {0}~\n'.format(self.maxwillpower))
            thefile.write('currentwillpower | {0}~\n'.format(self.currentwillpower))
            thefile.write('totalmemoryslots | {0}~\n'.format(dictWrite(self.totalmemoryslots)))
            thefile.write('memorizedspells | {0}~\n'.format(dictWrite(self.memorizedspells)))
            thefile.write('hitroll | {0}~\n'.format(self.hitroll))
            thefile.write('damroll | {0}~\n'.format(self.damroll))
            thefile.write('wimpy | {0}~\n'.format(self.wimpy))
            thefile.write('title | {0}~\n'.format(self.title))
            thefile.write('guild | {0}~\n'.format(self.guild))
            thefile.write('council | {0}~\n'.format(self.council))
            thefile.write('family | {0}~\n'.format(self.family))
            thefile.write('clan | {0}~\n'.format(self.clan))
            thefile.write('deity | {0}~\n'.format(self.deity))
            thefile.write('skillpoints | {0}~\n'.format(self.skillpoints))
            thefile.write('seen as | {0}~\n'.format(self.seen_as))
            thefile.write('maximum stat | {0}~\n'.format(dictWrite(self.maximum_stat)))
            thefile.write('current stat | {0}~\n'.format(dictWrite(self.current_stat)))
            thefile.write('discipline | {0}~\n'.format(self.discipline))
            thefile.write('aesthetic | {0}~\n'.format(self.aesthetic))
            thefile.write('exp | {0}~\n'.format(dictWrite(self.exp)))
            thefile.write('inventory | {0}~\n'.format(listWrite(self.inventory)))
            thefile.write('worn | {0}~\n'.format(dictWrite(self.worn)))
            thefile.write('baceac | {0}~\n'.format(dictWrite(self.baceac)))
            thefile.write('currentac | {0}~\n'.format(dictWrite(self.currentac)))
            thefile.write('hunger | {0}~\n'.format(self.hunger))
            thefile.write('thirst | {0}~\n'.format(self.thirst))
            thefile.write('position | {0}~\n'.format(self.position))
            thefile.write('aid | {0}~\n'.format(self.aid))
            thefile.write('known people | {0}~\n'.format(dictWrite(self.knownpeople)))
            thefile.write('prompt | {0}~\n'.format(self.prompt))
            thefile.write('alias | {0}~\n'.format(dictWrite(self.alias)))

    def interp(self, inp=None):
        inp = inp.split()
        isBuilding = hasattr(self, 'building')
        isEditing = hasattr(self, 'editing')
        self.oocflags['afk'] = False

        if len(inp) == 0:
            if isBuilding and not isEditing:
                self.write(self.building.display())
                return
            if isEditing:
                self.editing.add('')
                return
            else:
                self.write('')
                return

        if len(inp) != 0:
            if inp[0] in list(self.alias.keys()):
                inp[0] = self.alias[inp[0]]
                
        comfind = []
        if len(inp) <= 0:
            inp = ['']     # Added for OLC code to operate properly.
        for item in sorted(commands.commandhash.keys()):
            if item.startswith(inp[0].lower()):
                comfind.append(commands.commandhash[item])
        if isBuilding:
            types = {helpsys.oneHelp: 'helpedit',
                     races.oneRace: 'raceedit',
                     commands.Command: 'cedit',
                     area.oneArea: 'areaedit',
                     room.oneRoom: 'roomedit',
                     exits.Exit: 'exitedit'}
            if self.building.__class__ in list(types.keys()):
                comfind.append(commands.commandhash[types[self.building.__class__]])
                inp.reverse()
                inp.append(types[self.building.__class__])
                inp.reverse()
                self.write('')
        if len(comfind) > 0:
            try:
                if isEditing:
                    comfind[-1].call(self, ' '.join(inp[1:]))
                elif isBuilding:
                    if comfind[0].name not in types.values():
                        comfind[0].call(self, ' '.join(inp[2:]))
                    else:
                        comfind[0].call(self, ' '.join(inp[1:]))
                else:
                    comfind[0].call(self, ' '.join(inp[1:]))
            except (NameError, IndexError) as msg:
                self.write(msg)
        else:
            self.write("Huh?")

    def isadmin(self):
        if 'admin' in self.capability:
            return True
        else:
            return False
        
    def isdeity(self):
        if 'deity' in self.capability:
            return True
        else:
            return False
        
    def isbuilder(self):
        if 'builder' in self.capability:
            return True
        else:
            return False
    
    def isplayer(self):
        if 'player' in self.capability:
            return True
        else:
            return False
            
    # This doesn't belong here, put somewhere else.
    def statWords(self, statvalue = 55):
        if statvalue < 40:
            return "abismal"
        elif statvalue <= 44:
            return "terrible"
        elif statvalue <= 49:
            return "bad"
        elif statvalue <= 54:
            return "poor"
        elif statvalue <= 59:
            return "average"
        elif statvalue <= 64:
            return "fair"
        elif statvalue <= 69:
            return "good"
        elif statvalue <= 74:
            return "excellent"
        else:
            return "amazing"
