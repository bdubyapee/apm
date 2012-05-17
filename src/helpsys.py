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
# Filename: help.py
# 
# File Description: Module to handle the help system.


import os
import glob
import time

import olc
from fileparser import flatFileParse, listWrite, listRead, textRead
from fileparser import dictWrite, dictRead, boolRead, boolWrite
import world


sections = ('player', 'immortal', 'builder', 'deity')


class oneHelp(olc.Editable):
    def __init__(self, path):
        olc.Editable.__init__(self)
        self.path = path
        self.builder = None
        self.creator = ''
        self.viewable = ''
        self.keywords = []
        self.topics = ''
        self.section = ''
        self.description = ''
        self.commands = {'viewable': ('string', ['true', 'false']),
                         'creator': ('string', None),
                         'keywords': ('list', None),
                         'topics': ('string', None),
                         'section': ('string', sections),
                         'description': ('description', None)}

        if os.path.exists(path):
            self.load()

    def load(self):
        dictinfo = flatFileParse(self.path)
        self.creator = dictinfo['creator']
        self.viewable = dictinfo['viewable']
        self.keywords = listRead(dictinfo['keywords'])
        self.topics = dictinfo['topics']
        self.section = dictinfo['section']
        self.description = dictinfo['description']

    def save(self):
        with open(self.path, 'w') as thefile:
            thefile.write('creator | {0}~\n'.format(self.creator))
            thefile.write('viewable | {0}~\n'.format(self.viewable.lower()))
            thefile.write('keywords | {0}~\n'.format(listWrite(self.keywords)))
            thefile.write('topics | {0}~\n'.format(self.topics))
            thefile.write('section | {0}~\n'.format(self.section))
            thefile.write('description | {0}~\n'.format(self.description))

    def display(self):
        retvalue = "{{WCreator{{x: {0}\n"\
                   "{{WViewable{{x: {1}\n"\
                   "{{WKeywords{{x: {2}\n"\
                   "{{WRelated Topics{{x: {3}\n"\
                   "{{WSection{{x: {4}\n"\
                   "{{WDescription{{x:\n\r"\
                   "{5}|...\n\r".format(
                      self.creator, self.viewable, self.keywords,
                      self.topics,self.section, self.description[:180])
        return retvalue

helpfiles = {}

def init():
    allhelps = glob.glob(os.path.join(world.helpDir, '*'))
    for singlehelp in allhelps:
        thehelp = oneHelp(singlehelp)
        for keyword in thehelp.keywords:
            helpfiles[keyword] = thehelp

def reload():
    helpfiles = {}
    init()

def get_help(key, server=False):
    key = key.lower()
    if key != '':
        if key in helpfiles:
            if helpfiles[key].viewable.lower() == 'true' or server == True:
                return helpfiles[key].description
        else:
            filename = '{0}\\missinghelp'.format(world.logDir)
            with open(filename, 'a') as thefile:
                thefile.write('{0}> {1}\n'.format(time.asctime(), key))
            return 'We do not appear to have a help file for '\
                   'that topic.  We have however logged the attempt '\
                   'and will look into creating a help file for that '\
                   'topic as soon as possible.\n\r'