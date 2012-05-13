#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: comm.py
# 
# File Description: Communications Module.  Handles low level channel/log stuff.
# 
# By: admin

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