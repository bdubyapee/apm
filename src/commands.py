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
# Filename: commands.py
# 
# File Description: Commands module


import os
import glob
import time

import olc
import color
from fileparser import flatFileParse, listWrite, listRead, textRead
from fileparser import dictWrite, dictRead, boolRead, boolWrite
import area
import exits
import helpsys
import comm
import login
import races
import room
import world
import player
import livingthing
import apmserver

commandhash = {}

def evaluator(compiledobject, themap={}):
    themap.update({'__builtins__':None})
    try:
        rv = eval(compiledobject, themap, {})
    except NameError as ne:
        return
    return rv

# Define some mappings here to use in commands and scripts.
# We will want to create an object that holds modifiable data without
# giving them access to the objects themselves.  Shouldn't be too hard
# as long as we think through what all they will need, and what they will
# need to do it to.  XXX
_genericmaps = {'server':apmserver,
                'color':color,
                'player':player,
                'livingthing': livingthing,
                'login':login,
                'commandhash':commandhash,
                'helpsys':helpsys,
                'comm':comm,
                'races':races,
                'olc':olc,
                'area':area,
                'exits':exits,
                'world':world,
                'time': time,
                'room':room,
                'open': open,
                'os': os,
                'len':len,
                'range': range,
                'int': int,
                'dir': dir,
                'str': str,
                'hasattr':hasattr,
                'True':True,
                'False':False}


def init():
    allcommands = glob.glob(world.commandDir + "\\*")
    for eachcommand in allcommands:
        newcommand = Command(eachcommand)
        commandhash[newcommand.name] = newcommand

_capabilities = ('player', 'builder', 'deity', 'admin')

class Command(olc.Editable):
    def __init__(self, path):
        olc.Editable.__init__(self)
        self.path = path
        self.builder = None
        self.name = ''
        self.capability = ''
        self.description = ''
        self.compiled = None
        self.disabled = False
        self.racelim = []
        self.classlim = []
        self.skilllim = {}
        self.noview = False
        self.commands = {'name': ('string', None),
                         'capability': ('string', _capabilities),
                         'description': ('description', None),
                         'disabled': ('string', ['true', 'false']),
                         'racelim': ('list', None),
                         'classlim': ('list', None),
                         'skilllim': ('dict', (None, None)),
                         'noview': ('string', ['true', 'false'])}
        if os.path.exists(self.path):
            self.load()

    def load(self):
        dictinfo = flatFileParse(self.path)
        self.name = dictinfo['name']
        self.capability = dictinfo['capability']
        self.description = dictinfo['description']
        self.disabled = dictinfo['disabled']
        self.racelim = listRead(dictinfo['racelim'])
        self.classlim = listRead(dictinfo['classlim'])
        self.skilllim = dictRead(dictinfo['skilllim'])
        self.noview = dictinfo['noview']
        try:
            self.compiled = compile(self.description, 'tmp', 'exec')
        except Exception as msg:
            print("Error compiling {0}.\n{1}\n".format(self.name, msg))
            self.disabled = 'true'

    def save(self):
        with open(self.path, 'w') as thefile:
            thefile.write('name | {0}~\n'.format(self.name))
            thefile.write('capability | {0}~\n'.format(self.capability))
            thefile.write('description | {0}~\n'.format(self.description))
            thefile.write('disabled | {0}~\n'.format(self.disabled))
            thefile.write('racelim | {0}~\n'.format(listWrite(self.racelim)))
            thefile.write('classlim | {0}~\n'.format(listWrite(self.classlim)))
            thefile.write('skilllim | {0}~\n'.format(dictWrite(self.skilllim)))
            thefile.write('noview | {0}~\n'.format(self.noview))

    def display(self):
        retvalue = "Name: {0}\n\r"\
                   "Capability: {1}\n\r"\
                   "Disabled: {2}\n\r"\
                   "Race Limit: {3}\n\r"\
                   "Class Limit: {4}\n\r"\
                   "Skill Limits: {5}\n\r"\
                   "Viewable: {6}\n\r"\
                   "\n\r"\
                   "Description:\n\r"\
                   "{7}...\n\r".format(
                      self.name, self.capability, self.disabled,
                      self.racelim, self.classlim, self.skilllim,
                      self.noview, self.description[:180])
        return retvalue

    def call(self, caller, args):
        if self.capability in caller.capability:
            if self.disabled == 'false':
                localmaps = {}
                localmaps.update(_genericmaps)
                localmaps.update({'caller':caller})
                localmaps.update({'args':args})
                evaluator(self.compiled, localmaps)
            else:
                caller.write("I'm sorry, that command is temporarily disabled.")
                return
        else:
            caller.write("Huh?")
