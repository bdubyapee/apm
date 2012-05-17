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
# Filename: comm.py
# 
# File Description: Communications Module.  Handles low level channel/log stuff.


import time

import player

def wiznet(msg=''):
    msg = "\n\r\n\r{{YWiznet: {0}{1}{{x".format(msg.capitalize()[0], msg[1:])
    [person.write(msg) for person in player.playerlist if person.isadmin()]
        
def act():
    pass

def log(tofile=None, msg=''):
    if tofile == None:
        wiznet("Trying to log to no file in comm.py: {0}".format(msg))
        return
    else:
        with open(tofile, 'a') as tofile:
            tofile.write("{0} : {1}\n\r".format(time.ctime(), msg))