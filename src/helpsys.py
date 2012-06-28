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

"""Filename: helpsys.py
 
File Description: This module is the in-game help system.  Players can "help <keyword(s)>" to receive a help file display.
                  The help files are stored in text files.  They can be modified and reloaded 'on the fly' as the class inherits
                  from the olc.Editable class.
               
                  
Public variables:
    helpfiles -- a dictionary that contains keyword to helpfile content mappings.
        

Public functions:
    init() : 
        Accepts: Nothing
        Returns: Nothing
            Opens up all of the help files and reads in the data to build the help system.
            
    reload() : 
        Accepts: Nothing
        Returns: Nothing
            This is a cheater function to reload all of the help files without shutting the game down.
            
    get_help(key, server=False) :
        Accepts: keyword arguments in a string (key), if the server is calling and not a player (server)
        Returns: returns a string of the help data, or a string error message indicating that the help doesn't exist
            This is the main function, it takes keyword arguments.  If it finds a matching help entry it returns
            a string of the help information.  If it does not find the keyword, it logs the missing file and informs
            the player.


Public classes:
    oneHelp(olc.Editable)
            

Private variables:
    _sections -- A set holding strings of the help file 'sections'


Private functions:
    None


Private classes:
    None

"""

import os
import glob
import time

import olc
from fileparser import flatFileParse, listWrite, listRead, textRead
from fileparser import dictWrite, dictRead, boolRead, boolWrite
import world


_sections = ('player', 'immortal', 'builder', 'deity')


class oneHelp(olc.Editable):
    """oneHelp(olc.Editable):           
         NOTES:  The inheritance from olc.Editable provides our in-game manipulation interface.  The
                 public methods exposed by this class are named and operate specifically to accommodate
                 that modules needs.  Any "thing" that inherits from olc.Editable will have this interface
                 and will therefor be editable in-game.

        Arguments:
            path -- a string of the helpfile path location
            
        Public Methods:
            save(self):
                Arguments: None
                Return Type: a string
                     Creates a string representation of the helpfile data.  Opens the file for writing, and writes the data.
                     
            load(self):
                Arguments: Nothing
                Return Type: Nothing
                     Loads the help file data using the path in self.path.  Reads the file and populates the isntance variables
                     for that particular helpfile.
                     
            display(self):
                Arguments: None
                Return Type: str
                    Returns a string representation of the helpfile data.

                    
    """
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
                         'section': ('string', _sections),
                         'description': ('description', None)}

        if os.path.exists(path):
            self.load()

    def load(self):
        """ Open the area data file located at self.path.  Assigns the data read into the instance
            variables.
        
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
        self.creator = dictinfo['creator']
        self.viewable = dictinfo['viewable']
        self.keywords = listRead(dictinfo['keywords'])
        self.topics = dictinfo['topics']
        self.section = dictinfo['section']
        self.description = dictinfo['description']

    def save(self):
        """ Write all of our helpfile information out to a file(self.path)
        
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
            thefile.write('creator | {0}~\n'.format(self.creator))
            thefile.write('viewable | {0}~\n'.format(self.viewable.lower()))
            thefile.write('keywords | {0}~\n'.format(listWrite(self.keywords)))
            thefile.write('topics | {0}~\n'.format(self.topics))
            thefile.write('section | {0}~\n'.format(self.section))
            thefile.write('description | {0}~\n'.format(self.description))

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
conn = sqlite3.connect((os.path.join(world.dataDir, 'helps.sqlite')))

def init():
    """ The initialization function for the helpsystem.  Glob a list of all helpfile file names
        read in each one at a time and pass as init data to oneHelp, then adding keyword to data
        mappings to helpfiles.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """  
    allhelps = glob.glob(os.path.join(world.helpDir, '*'))
    for singlehelp in allhelps:
        thehelp = oneHelp(singlehelp)
        for keyword in thehelp.keywords:
            helpfiles[keyword] = thehelp
    

def reload():
    """ This is a cheater function used to reload all of the helpfiles.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """  
    helpfiles = {}
    init()

def get_help(key, server=False):
    """ Receive keyword argument(s) and a bool of whether or not this is an internal server help call.
        Look for the keywords indicated, if the help file is found, return the string.  If not found,
        make a note in the log about the missing helpfile and return a string indicating that it is missing.
    
    Keyword arguments:
        key : string
            This is a string representation of keyword(s) the user is looking for.
        server : Bool
            This lets us know if it is an internal server call to the helpsystem.  We use this to do things like
            display the MOTD, display race/class information during login and creation.
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """  

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