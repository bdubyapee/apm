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

"""Filename: fileparse.py
 
File Description: This utility module houses functions that are used in the flat file format
                  utilized to store area and player information.  I have been looking at potentially
                  moving to a SQL/NOSQL type solution for this structured information.  Perhaps
                  in the next revision.  XXX
               
                  
Public variables:
    None
        

Public functions:
    flatFileParse(string) : returns a dictionary mapping
    listWrite(list) : returns a string representation of a list
    textRead(string) : returns a string that has been stripped
    listRead(string) : returns a list that was stored as a string
    dictWrite(dict) : returns a string representation of a dict
    dictRead(text) : returns a dict that was stored as a string
    boolRead(text) : returns True or False
    boolWrite(bool) : returns 'True' or 'False' string

Public classes:
    None
            

Private variables:
    None    


Private functions:
    None


Private classes:
    None

"""

def flatFileParse(thepath):
    """ Takes a file path as an argument.  Opens and reads the text file containing area/player data.
        Takes that read in string information, strips the strings and builds a dictionary out of the key->value
        pairs.  Returns the dictionary.
        
        Keyword arguments:
            thepath -- a string that represents a file path
            
        Return value:
            dict : A dictionary of key->value pairs of the data read from the file.
            
        Example:
            Input : "c:\playerfile.txt"
            Output : {'Name' : 'Jubelo',
                      'Level' : 15,
                      'BodyParts' : ['head', 'arms']}
            
        Additional notes:
            None
            
    """
    with open(thepath, 'r') as thefile:
        data = thefile.read()
    
    data = [item.strip() for item in data.split('~') if item.strip() != '']
    dictinfo = {}
    for thing in data:
        first = thing.index('|')
        dictinfo[thing[:first].strip()] = thing[first + 1:].strip()
    return dictinfo

def listWrite(thelist):
    """ Takes a list as an argument, converts this to a string representation and returns it.
        
        Keyword arguments:
            thelist -- a list
            
        Return value:
            string : A string representation of a list
            
        Example:
            Input : [1, 'two']
            Output : "1, two"
            
        Additional notes:
            None
            
    """
    output = []
    for item in thelist:
        output.append(str(item))
    return ', '.join(output)
        
def textRead(thestring):
    """ Takes a string as an argument, strips it, and returns it.
        
        Keyword arguments:
            thetext -- a string
            
        Return value:
            string : A string that has been stripped
            
        Example:
            Input : " 1, two     "
            Output : "1, two"
            
        Additional notes:
            None
            
    """
    return thestring.strip()
        
def listRead(thestring):
    """ Takes a string as an argument.  Converts it to a list and returns the list.
        
        Keyword arguments:
            thelist -- a string
            
        Return value:
            list : Returns a string split up into a list.
            
        Example:
            Input : "1, two, 3, four"
            Output : ['1', 'two', '3', 'four']
            
        Additional notes:
            None
            
    """
    return [i.strip() for i in thestring.split(',') if len(i.strip()) > 0]

def dictWrite(thedict):
    """ Takes a dict as an argument, returns a string representation of the dict.
        
        Keyword arguments:
            thedict -- a dictionary
            
        Return value:
            string : A string representation of a dict
            
        Example:
            Input : {1 : 'one', 2 : 'two'}
            Output : "1 : one, 2 : two"
            
        Additional notes:
            None
            
    """
    retvalue = []
    for key in list(thedict.keys()):
        if type(thedict[key]) == type([]):
            thedict[key] = ' '.join(thedict[key])
            if len(thedict[key]) <= 0:
                thedict.pop(key)
                return
        retvalue.append('{0} : {1}'.format(key, thedict[key]))
    return ','.join(retvalue)

def dictRead(thestring):
    """ Takes a string representation of a dict as an argument, converts it to a dict type and returns it.
        
        Keyword arguments:
            thestring -- a string
            
        Return value:
            dict : A dictionary built out of the string
            
        Example:
            Input : "1 : one, 2 : two"
            Output : {1 : 'one', 2 : 'two'}
            
        Additional notes:
            None
            
    """
    retvalue = {}
    items = thestring.split(',')
    for item in items:
        if item != '':
            retvalue[item.split(':')[0].strip()] = item.split(':')[1].strip()
    return retvalue

def boolRead(thestring):
    """ Takes a string as an argument, returns a Bool of True or False depending on the string.
        
        Keyword arguments:
            thestring -- a string
            
        Return value:
            bool : A boolean representation of text
            
        Example:
            Input : "true"
            Output : True
            
        Additional notes:
            None
            
    """
    if thestring.lower() == 'true':
        return True
    else:
        return False

def boolWrite(thebool):
    """ Takes a boolean as an argument.  Returns a test representation of the boolean.
        
        Keyword arguments:
            thebool -- a boolean
            
        Return value:
            string : A string representation of a boolean
            
        Example:
            Input : False
            Output : "false"
            
        Additional notes:
            None
            
    """
    if thebool == True:
        return 'true'
    else:
        return 'false'
