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

"""Filename: area.py
 
File Description: Module handling area information.  Functionality is provided to load and save area files.
                  Each Area instance inherits from the olc module which allows in-game editing of the objects.
                  We keep lists of areas, rooms, mobiles and game objects here.  These are index lists of master
                  object copies, we will need to implement seperate lists for 'in-game' mobiles and objects.
                  
                  For example, an area has it's list of objects and mobiles.  If a player obtains a standard
                  short sword we can reference that to the master item.  If the pleyer puts a +1 to damage (in some
                  way) on that item, we need to be able to keep that seperatly from the master item so not all
                  new short swords have a +1 associated with them.  XXX More to come on this.
               
                  
Public variables:
    arealist : list
        A list containing a reference to each Area instance.
    roomlist : dictionary
        A dictionary containing a mapping from VNUM (internal reference number) to a room instance.
    mobilelist : dictionary
        A dictionary containing a mapping from VNUM (internal reference number) to a mobile instance.
    objectlist : dictionary
        A diationary containing a mapping from VNUM (internal reference number) to an object instance.
    planes : set
        A set containing the names of the planes of existance.
    difficulty : set
        A set containing the names of the difficulty level associated with the area
        

Public functions:
    init() : return nothing
    
    roomByVnum(vnum) : 
        Accepts: vnum - int
        Returns: Room object or False


Public classes:
    oneArea(olc.Editable)
            

Private variables:
    None


Private functions:
    None


Private classes:
    None

"""


import os
import re
import glob

import olc
import room
import event
import world
import player
import mobile


arealist = []
roomlist = {}
mobilelist = {}
objectlist = {}

def init():
    """ Uses the configuration variable world.areaDir to build a list of area files.  Loops through each area
        file location and passes the path to the oneArea class to create an instance.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Additional notes:
        None
        
    """
    areas = glob.glob(os.path.join(world.areaDir, '*'))
    for areapath in areas:
        newarea = oneArea(areapath)

def roomByVnum(vnum):
    """ Accept an integer, attempts to use that int as an index value to the roomlist value.
    
    Keyword arguments:
        vnum  --  a int type
        
    Return value:
        return -- a Room object or False
        
    Example:
        input = 317
        return value = Room object located by roomlist[317]
        
    Additional notes:
        The roomlist dictionary is a public value in (this) the area.py module.
        
    """
    if vnum in roomlist.keys():
        return roomlist[vnum]
    else:
        return False

_headerRe = re.compile(r'Header(.*?)ENDHeader', re.I | re.S)
_roomsRe = re.compile(r'Rooms(.*?)ENDRooms', re.I | re.S)
_mobsRe = re.compile(r'Mobs(.*?)ENDMobs', re.I | re.S)
_objectsRe = re.compile(r'Objects(.*?)ENDObjects', re.I | re.S)
_resetsRe = re.compile(r'Resets(.*?)ENDResets', re.I | re.S)
_shopsRe = re.compile(r'Shops(.*?)ENDShops', re.I | re.S)

planes = ('material',)

difficulty = ('all', 'very easy', 'easy', 'moderate', 'hard', 'very hard', 'extreme')

class oneArea(olc.Editable):
    """oneArea(olc.Editable):
        NOTES:  The inheritance from olc.Editable provides our in-game manipulation interface.  The
                public methods exposed by this class are named and operate specifically to accommodate
                that modules needs.  Any "thing" that inherits from olc.Editable will have this interface
                and will therefor be editable in-game..
                
        Arguments:
            Accepts a string value as argument providing an absolute path to the area file to load.
            
        Public Methods:
            savedata(self)
                Arguments: None
                Return Type: string
                    Returns string data representing the area specific data (header)
                
            loaddata(self, data):
                Arguments: data - 'str'
                Return Type: Nothing
                     Receives a string containing area header data, processes the data and assigns
                     the data to the isntance variables.
                
            load(self):
                Arguments: None
                Return Type: Nothing
                     Uses the isntance variable self.path, opens the text file and reads in the data.
                     Uses the private regex objects to idenfity different portions of the area file.
                     Calls isntance methods of each object type associated with the data type found and passes
                     that data to those methods for processing.
                     
            save(self):
                Arguments: None
                Return Type: Nothing
                     Uses instance variable self.path, opens a file for writing the area data to.  Places
                     the section tags around area data pulled from the objects associated with the area.
                     
            display(self):
                Arguments: None
                Return Type: str
                    Returns a string representation of the area header data.
                    
    """
    def __init__(self, path):
        olc.Editable.__init__(self)
        self.path = path
        self.name = ''
        self.author = ''
        self.plane = ''
        self.hometown = ''
        self.difficulty = ''
        self.alignment = ''
        self.locationx = 0
        self.locationy = 0
        self.vnumlow = -1
        self.vnumhigh = -1
        self.roomlist = {}
        self.moblist = {}
        self.objectlist = {}
        self.mobindexlist = {}
        self.objectindexlist = {}
        self.resetlist = []
        self.shoplist = []
        self.playerlist = []
        self.events = []
        event.init_events_area(self)
        self.commands = {'name': ('string', None),
                         'author': ('string', None),
                         'plane': ('string', planes),
                         'hometown': ('string', None),
                         'difficulty': ('string', difficulty),
                         'alignment': ('string', None),
                         'locationx': ('integer', None),
                         'locationy': ('integer', None),
                         'vnumlow': ('integer', None),
                         'vnumhigh': ('integer', None)}
        if os.path.exists(self.path):
            self.load()
            arealist.append(self)

    def savedata(self):
        """ Generates a string containing the area(object) header data and returns it.
        
        Keyword arguments:
            None
            
        Return value:
            return -- a string object containing header data.
            
        Example:
            None
            
        Additional notes:
            None
            
        """        
        retdata = "name | {0}~\n"\
                  "author | {1}~\n"\
                  "plane | {2}~\n"\
                  "hometown | {3}~\n"\
                  "difficulty | {4}~\n"\
                  "alignment | {5}~\n"\
                  "locationx | {6}~\n"\
                  "locationy | {7}~\n"\
                  "vnum low | {8}~\n"\
                  "vnum high | {9}~\n".format(
                     self.name, self.author, self.plane, self.hometown, 
                     self.difficulty, self.alignment, self.locationx,
                     self.locationy, self.vnumlow, self.vnumhigh)
        return retdata

    def loaddata(self, data):
        """ Accepts string data, processes it and loads it into instance variables.
        
        Keyword arguments:
            data  --  a 'str' type
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            We receive string data.  Convert to int where necessary.
            
        """        
        data = [item.strip() for item in data if item.strip() != '']
        dictinfo = {}
        for thing in data:
            first = thing.index('|')
            dictinfo[thing[:first].strip()] = thing[first + 1:].strip()
        self.name = dictinfo['name']
        self.author = dictinfo['author']
        self.plane = dictinfo['plane']
        self.hometown = dictinfo['hometown']
        self.difficulty = dictinfo['difficulty']
        self.alignment = dictinfo['alignment']
        self.locationx = int(dictinfo['locationx'])
        self.locationy = int(dictinfo['locationy'])
        self.vnumlow = int(dictinfo['vnum low'])
        self.vnumhigh = int(dictinfo['vnum high'])

    def save(self):
        """ Write all of our area information out to a file(self.path)
        
        Keyword arguments:
            None
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            We write the section tag information then write data to the file.
            
        """        
        with open(self.path, 'w') as thefile:
            thefile.write('Header\n')
            thefile.write(self.savedata())
            thefile.write('ENDHeader\n\n')
            thefile.write('Rooms\n')
            for room in self.roomlist.keys():
                thefile.write(self.roomlist[room].savedata())
                thefile.write('$\n')
            thefile.write('ENDRooms\n\n')
            thefile.write('Mobs\n')
            if len(self.moblist) > 0:
                for mob in self.moblist:
                    thefile.write(mob.savedata())
                    thefile.write('$\n')
            thefile.write('ENDMobs\n\n')
            thefile.write('Objects\n')
            if len(self.objectlist) > 0:
                for oneobject in self.objectlist:
                    thefile.write(oneobject.savedata())
                    thefile.write('$\n')
            thefile.write('ENDObjects\n\n')
            thefile.write('Resets\n')
            if len(self.resetlist):
                for reset in self.resetlist:
                    thefile.write(reset.savedata())
                    thefile.write('$\n')
            thefile.write('ENDResets\n\n')
            thefile.write('Shops\n')
            if len(self.shoplist) > 0:
                for shop in self.shoplist:
                    thefile.write(shop.savedata())
                    thefile.write('$\n')
            thefile.write('ENDShops\n\n')

    def load(self):
        """ Open the area data file located at self.path.  Using the regular expression objects we
            identify different sections of information.  We then isolate that data and pass it to
            the appropriate methods to load it.
        
        Keyword arguments:
            None
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            XXX
            
        """        
        with open(self.path, 'r') as thefile:
            data = thefile.read()
            
        # Match the header information section.  Use self.loaddata to process.
        headmatch = _headerRe.search(data)
        if headmatch is not None:
            self.loaddata(headmatch.group(1).split('~'))
        else:
            print("Error matching header in {0}!".format(self.path))
            
        # Match the room information.  Load into room.oneRoom.
        roomsmatch = _roomsRe.search(data)
        if roomsmatch is not None:
            roomlist = [item.strip() for item in
                        roomsmatch.group(1).split('$') if item.strip() != '']
            for eachroom in roomlist:
                room.oneRoom(self, eachroom)
        else:
            print("Error matching rooms in {0}!".format(self.path))
            
        # Match the mobile (NPC) information.  Not Implemented yet.
        mobsmatch = _mobsRe.search(data)
        if mobsmatch is not None:
            moblist = [item.strip() for item in
                       mobsmatch.group(1).split('$') if item.strip() != '']
            for mob in moblist:
                pass
        else:
            print("Error matching mobs in {0}!".format(self.path))
            
        # Match the object (game object) information.  Not implemented yet.
        objsmatch = _objectsRe.search(data)
        if objsmatch is not None:
            objectlist = [item.strip() for item in
                          objsmatch.group(1).split('$') if item.strip() != '']
            for object in objectlist:
                pass
        else:
            print("Error matching objects in {0}!".format(self.path))
         
        # Match the reset data.  Not Implemented yet.   
        resetsmatch = _resetsRe.search(data)
        if resetsmatch is not None:
            resetlist = [item.strip() for item in
                         resetsmatch.group(1).split('$') if item.strip() != '']
            for reset in resetlist:
                pass
        else:
            print("Error matching resets in {0}!".format(self.path))
        
        # Match shop data.  Not Implemented yet.    
        shopsmatch = _shopsRe.search(data)
        if shopsmatch is not None:
            shoplist = [item.strip() for item in
                        shopsmatch.group(1).split('$') if item.strip() != '']
            for shop in shoplist:
                pass
        else:
            print("Error matching shoplist in {0}!".format(self.path))
        
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
        retvalue = "{{WName{{x: {0}\n"\
                   "{{WAuthor{{x: {1}\n"\
                   "{{WPlane{{x: {2}\n"\
                   "{{WHometown{{x: {3}\n"\
                   "{{WDifficulty{{x: {4}\n"\
                   "{{WAlignment{{x: {5}\n"\
                   "{{WLocation X{{x: {6}\n"\
                   "{{WLocation Y{{x: {7}\n"\
                   "{{WVnum Low{{x: {8}\n"\
                   "{{WVnum High{{x: {9}\n".format(
                      self.name, self.author, self.plane, self.hometown,
                      self.difficulty, self.alignment, self.locationx,
                      self.locationy, self.vnumlow, self.vnumhigh)
        return retvalue