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

"""Filename: exits.py
 
File Description: This module houses the code to handle rooms.  This will be seperate from any code
                  dealing with the 'wilderness' ASCII map.
               
                  
Public variables:
    None
        

Public functions:
    None
    

Public classes:
    Exit(olc.editable)
            

Private variables:
    _directions -- a set that contains strings representing the various directions available.
    _exitsizes -- a set that contains strings representing the exit sizes available.
    _oppositedirections -- a dict that maps a direction key, with a value that is the opposite.
    


Private functions:
    None


Private classes:
    None

"""


import olc
import area
import event

_directions = ('north', 'south', 'east', 'west', 'northwest', 'northeast',
               'southwest', 'southeast', 'up', 'down')

_exitsizes = ('huge', 'large', 'medium', 'tiny')

_oppositedirection = {'north': 'south',
                      'south': 'north',
                      'east': 'west',
                      'west': 'east',
                      'northwest': 'southeast',
                      'northeast': 'southwest',
                      'southwest': 'northeast',
                      'southeast': 'northwest',
                      'up': 'down',
                      'down': 'up'}

class Exit(olc.Editable):
    """Exit(olc.Editable):           
         NOTES:  The inheritance from olc.Editable provides our in-game manipulation interface.  The
                 public methods exposed by this class are named and operate specifically to accommodate
                 that modules needs.  Any "thing" that inherits from olc.Editable will have this interface
                 and will therefor be editable in-game.

        Arguments:
            None
            
        Public Methods:
            savedata(self):
                Arguments: None
                Return Type: a string
                     Creates a string representation of the exit data for use in writing to file and returns it.
                     
            load(self, data):
                Arguments: a string containing the exit data
                Return Type: Nothing
                     Takes a string argument, converts it's contents appropriatly and assigns the data to exit instance
                     variables.
                     
            display(self):
                Arguments: None
                Return Type: str
                    Returns a string representation of the exit data.

                    
    """
    def __init__(self, room, data=None):
        olc.Editable.__init__(self)
        self.room = room
        self.direction = ''
        self.destination = 0
        self.locked = 'false'
        self.lockdifficulty = 0
        self.keyvnum = 0
        self.magiclocked = 'false'
        self.physicaldiffuculty = 0
        self.magiclockdifficulty = 0
        self.casterid = 0
        self.magiclocktype = 'none'
        self.size = 'Huge'
        self.hasdoor = 'false'
        self.dooropen = 'true'
        self.keywords = []
        self.events = []
        event.init_events_exit(self)
        self.commands = {'direction': ('string', _directions),
                         'destination': ('integer', None),
                         'locked': ('string', ['true', 'false']),
                         'lockdifficulty': ('integer', None),
                         'keyvnum': ('integer', None),
                         'magiclocked': ('string', ['true', 'false']),
                         'physicaldifficulty': ('integer', None),
                         'magiclockdifficulty': ('integer', None),
                         'casterid': ('integer', None),
                         'magiclocktype': ('string', None),
                         'size': ('string', _exitsizes),
                         'hasdoor': ('string', ['true', 'false']),
                         'dooropen': ('string', ['true', 'false']),
                         'keywords': ('list', None)}
        if data is not None:
            self.load(data)

    def savedata(self):
        """ Converts all of the exit data for the instance into a string and returns it.
            Used to provide save data that can be written to the area file.
        
        Keyword arguments:
            None
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """
        thelist = [str(self.destination),
                   self.locked,
                   str(self.lockdifficulty),
                   str(self.keyvnum),
                   self.magiclocked,
                   str(self.physicaldifficulty),
                   str(self.magiclockdifficulty),
                   str(self.casterid),
                   self.magiclocktype,
                   self.size,
                   self.hasdoor,
                   self.dooropen,
                   ', '.join(self.keywords)]
        output = ' '.join(thelist)
        return output

    def load(self, data):
        """ Accepts a string type argument that is split up, and assigned to the exit instance.
        
        Keyword arguments:
            data -- a string type providing exit data.
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """
        data = data.split()
        self.direction = data[0]
        self.destination = int(data[1])
        self.locked = data[2]
        self.lockdifficulty = int(data[3])
        self.keyvnum = int(data[4])
        self.magiclocked = data[5]
        self.physicaldifficulty = int(data[6])
        self.magiclockdifficulty = int(data[7])
        self.casterid = int(data[8])
        self.magiclocktype = data[9]
        self.size = data[10]
        self.hasdoor = data[11]
        self.dooropen = data[12]
        self.keywords = data[13:]

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
        retvalue = "{{WRoom{{x: {0}\n"\
                   "{{WDirection{{x: {1}\n"\
                   "{{WDestination{{x: {2}\n"\
                   "{{WLocked{{x: {3}\n"\
                   "{{WLock Difficulty{{x: {4}\n"\
                   "{{WKey Vnum{{x: {5}\n"\
                   "{{WMagic Locked{{x: {6}\n"\
                   "{{WPhysical Difficulty{{x: {7}\n"\
                   "{{WMagic Lock Difficulty{{x: {8}\n"\
                   "{{WCaster ID{{x: {9}\n"\
                   "{{WMagic Lock Type{{x: {10}\n"\
                   "{{WSize{{x: {11}\n"\
                   "{{WHas Door{{x: {12}\n"\
                   "{{WDoor Open{{x: {13}\n"\
                   "{{WKeywords{{x: {14}\n".format(
                      self.room.name, self.direction, self.destination,
                      self.locked, self.lockdifficulty, self.keyvnum,
                      self.magiclocked, self.physicaldifficulty,
                      self.magiclockdifficulty, self.casterid, 
                      self.magiclocktype, self.size, self.hasdoor,
                      self.dooropen, self.keywords)
        return retvalue