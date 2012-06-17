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

"""Filename: commands.py
 
File Description: This module handles all in-game commands.  There are some important notes to take
                  into consideration here.  All commands are stored as text files in the /data directory.
                  Upon game startup each of the commands are read in and compiled into objects. THIS PRESENTS
                  A SECURITY ISSUE.  My original thought is that admin characters are the only ones with
                  access to modify these files in-game.  This means unless an admin/coder account is hacked
                  or your host box is hacked there shouldn't be a security risk through the game.   Still,
                  use this at your own risk.  
                  
                  The benefits however, are that you can modify a command in-game or offline and then reload the
                  command without rebooting the game.  You can also enable or disable commands in-game without
                  interrupting game play.
               
                  
Public variables:
    commandhash : dict
        A hash containing a command name, key, and a compiled code object value.
        

Public functions:
    init() : return nothing
    
    evaluator(compiledobject, themap={}) : 
        Accepts: 
            compiledobject - Compiled code object
            themap - dict containing reference maps for the compiled code objects
        Returns:
            any results returned from the code object


Public classes:
    Command(olc.Editable)
            

Private variables:
    _genericmaps -- dict object containing mappings used in the compiled code objects
    _capabilities -- A set containing string values that represent the various character capabilities


Private functions:
    None


Private classes:
    None

"""

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
    """ Accepts a compiled code object, and any references in a map to pass to the object.  It then executes
        the code object and returns any results from its execution.
    
    Keyword arguments:
        compiledobject  --  a compiled ocde object for execution(evaluation)
        themap -- a dict containing additional reference mappings to pass to the object during evaluation.
        
    Return value:
        Any returned value(s) or references passed back to the function from the code evaluation
        
        
    Additional notes:
        It should be noted that this function can be a potential security risk.  It is generally accepted that
        there is no real, true way to use eval safely.  I have not performed any kind of security audit so
        utilize this particular command system at your own risk.  To date there have been no issues. XXX
        
    """
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
    """ Uses the configuration variable world.commandDir to load each in-game command. It creates a command object
        and stores the mapping in teh commandhash dict.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Additional notes:
        None
        
    """

    allcommands = glob.glob(world.commandDir + "\\*")
    for eachcommand in allcommands:
        newcommand = Command(eachcommand)
        commandhash[newcommand.name] = newcommand

_capabilities = ('player', 'builder', 'deity', 'admin')

class Command(olc.Editable):
    """Command(olc.Editable):
        NOTES:  The inheritance from olc.Editable provides our in-game manipulation interface.  The
                public methods exposed by this class are named and operate specifically to accommodate
                that modules needs.  Any "thing" that inherits from olc.Editable will have this interface
                and will therefor be editable in-game.
                
        Arguments:
            Accepts a string value as argument providing an absolute path to the command file to load.
            
        Public Methods:
            load(self):
                Arguments: None
                Return Type: Nothing
                     Uses the isntance variable self.path, opens the text file and reads in the data.
                     Assigns the instance variables from the command file and compiles the code itself
                     into a code object for execution 'on the fly'.  Mapping for additional values is
                     handled outside of the Class/Instance in the commands.py module.
                     
            save(self):
                Arguments: None
                Return Type: Nothing
                     Uses instance variable self.path, opens a file for writing the command data to.
                     
            display(self):
                Arguments: None
                Return Type: str
                    Returns a string representation of the command data.
                    
            call(self):
                Arguments: 
                    caller -- A player object instance (the person calling the command)
                    args -- a string with any arguments passed to the command from the player.
                Return Type: 
                    
    """
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
        """ Uses self.path to get a file location to load the command data.  Loads the data, assigns instance
            variables based on the data.  Compiles the code from from the file into a code object to be used
            in eval() when the command is called.
        
        Keyword arguments:
            None
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """
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
        """ Opens the file associated with the location in self.path and writes the command header data
            as well as the code to the command file.
        
        Keyword arguments:
            None
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """
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
        """ Create a string value that we can return to a caller function for use in the OLC.
        
        Keyword arguments:
            None
            
        Return value:
            return -- a 'str' object.
            
        Example:
            None
            
        Additional notes:
            None
            
        """        
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
        """ Call a command.  We take the caller and any arguments as parameters.  We check that the caller
            has the appropriate in-game permissions (capabilities) to execute the command.  We add in the
            necessary pre-mapped references as well as references to the args and caller and then evaluate
            the command, receiving any returned values back from the eval.
        
        Keyword arguments:
            caller -- a Player object instance, used for permission check as well as passed to the command.
            args -- a 'str' containing any arguments passed into the command.
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """        

        if self.capability in caller.capability:
            if self.disabled == 'false':
                localmaps = {}
                localmaps.update(_genericmaps)
                localmaps.update({'caller':caller})
                localmaps.update({'args':args})
                evaluator(self.compiled, localmaps)
            else:
                caller.write("I'm sorry, that command is temporarily disabled.")
        else:
            caller.write("Huh?")
