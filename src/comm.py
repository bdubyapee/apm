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

"""Filename: comm.py
 
File Description: Communications module to handle various channels and logging.
               
                  
Public variables:
    None


Public functions:
    wiznet(msg='') : 
        Accepts: msg - string
        Returns: None
    
    log(tofile=None, msg='') :
        Accepts: tofile - file object
                 msg - string
        Returns: None


Public classes:
    None


Private variables:
    None


Private functions:
    None


Private classes:
    None
    
"""

import time

import player

def wiznet(msg=''):
    """ Accepts a string to be sent to Administrator account users that are logged in.
    
    Keyword arguments:
        msg  --  a string type
        
    Return value:
        None
        
    Example:
        input = "A message for all Admins!"
        return value = None
        
    Additional notes:
        We accept a string to be sent to all logged in admins.  We append some carriage returns and new lines
        so the display formatting is correct.  We prepend the 'channel name' of Wiznet: to the message and give it
        yellow character color codes so it stands out.  Capitalize the first letter of the message itself and send.
        
    """
    msg = "\n\r\n\r{{YWiznet: {0}{1}{{x".format(msg.capitalize()[0], msg[1:])
    #[person.write(msg) for person in player.playerlist if person.isadmin()]
    for person in player.playerlist:
        if person.isadmin():
            person.write(msg)
        
def act():
    """ Currently a placeholder.  This will become a comm function that will make outgoing messages (to clients)
        gender and and contextually correct.  
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        input = ""
        return value = ""
        
    Additional notes:
        When something happens in the game, the output displayed to clients will be different depending on varying
        factors.  Lets say that I drop a sword.  I would expect to see on my client something like "You dropped a short sword".
        Others in the room should see a message dependant on their context.  For examples, "Jubelo dropped a short sword",
        "A dark shadowy figure dropped a short sword", "You hear someting drop to the ground".
        
        The message per client will be fully dependant on multiple conditions.  Can they see, do they know the person, are they
        under any kind of influence (Spell or skill for example).   It will take some planning and whiteboarding to determine
        exactly how to do this. XXX
        
    """
    pass

def log(tofile=None, msg=''):
    """ Accepts a file name and a log message to put in that file.
    
    Keyword arguments:
        tofile -- a string type
        msg  --  a string type
        
    Return value:
        None
        
    Example:
        input = "adminlog.txt", "Jubelo has left the game at 12:15:31 01/01/2013"
        return value = None
        
    Additional notes:
        We accept a string that contains the file name of the log file we are to write to. 
        We then open the file for appending, write the log message to the file and the file
        closes.  I don't like how we are constantly opening and closing files for doing this,
        if traffic is enough (or assuming we get alot of players on at once) the file access
        with opening and closing alone will cause us some problems.  Look into the logging module
        or some third party way of doing this.   Short of that at least rewrite the "Log related" 
        code so the files are opened upon game startup and messages are buffered and written as
        necessary. XXX
        
    """
    if tofile == None:
        wiznet("Trying to log to no file in comm.py: {0}".format(msg))
    else:
        with open(tofile, 'a') as tofile:
            tofile.write("{0} : {1}\n\r".format(time.ctime(), msg))