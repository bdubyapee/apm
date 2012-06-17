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

"""Filename: event.py
 
File Description: This module contains a simple, custom Event Queue.  This is used to provide
                  a way to 'fire' events on players, objects, rooms, etc.  This can happen once
                  at a predetermined time, or it can be configured as a reoccuring event.  The final
                  plan is to utilize this module to fire events such as player autosave, objects that
                  need to travel, such as carts, ships etc.  We can use this for any 'behind the scenes'
                  events, or events that directly affect the players/world.
               
                  
Public variables:
    allevents : Queue class instance.  All events in the queue are stored in a class variable so it is
                generally self contained.  Not sure if we want/need to change this any any point.
    PULSE_PER_SECOND : An int variable holding the number that corresponds to one second.
    PULSE_PER_MINUTE : An int variable holding the number that corresponds to one minute.
        

Public functions:
    * Startup / Initialization public functions *
    init() : return nothing
    heartbeat() : return nothing
    init_events_socket() : return nothing
    init_events_area() : return nothing
    init_events_server() : return nothing
    init_events_room() : return nothing
    init_events_exit() : return nothing
    init_events_mobile() : return nothing
    init_events_player() : return nothing
    init_events_object() : return nothing
    
    * These are actual reoccuring events that are default for each type at startup *
    event_player_autosave() : return nothing
    

Public classes:
    None
            

Private variables:
    _eventcache -- a list that contains 'empty' events.  The thought is to cache these for faster event creation.
    


Private functions:
    _getEvent()


Private classes:
    _Queue()
    _Event()

"""

import sys
import time

import player


class _Queue:
    """_Queue:           
        Arguments:
            None
            
        Public Methods:
            add(self, event):
                Arguments: event object
                Return Type: Nothing
                     Adds the event object to the master event list, as well as to the event list of the owner.
                     
            remove(self, event):
                Arguments: event object
                Return Type: Nothing
                     Removes an event object from the master event list, as well as the event list of the owner.
                     
            removePlayer(self, player):
                Arguments: player object
                Return Type: Nothing
                    Iterates over all of a players events, and removes them from the master event list. Used when
                    a player quits the game.
                    
            update(self):
                Arguments: None
                Return Type: None
                    Upon a call to this method, all events in the list have their passes decremented.  Once it is time
                    for an event to happen, the fire() method is called on the event itself.
                    
    """
    def __init__(self):
        self.eventlist = []

    def add(self, event):
        """ Adds an event to the master event list, as well as the event list for the owner object.
        
        Keyword arguments:
            event -- An event object type.
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """
        self.eventlist.append(event)
        event.owner.events.append(event)

    def remove(self, event):
        """ Removes an event from the master event list, as well as the event list for the owner object.
        
        Keyword arguments:
            event -- An event object type.
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """    
        event.owner.events.remove(event)
        self.eventlist.remove(event)

    def removePlayer(self, player):
        """ Removes all events from the master list that belong to the owner.
        
        Keyword arguments:
            Player -- A player object type.
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            Need to reword the variables here so this isn't as ambiguious if used to remove events from
            another 'owner'.  Such as a room, object, mobile etc. XXX
            
        """
        for item in player.events:
            self.remove(item)

    def update(self):
        """ Update function that is called to decrement the counters of events in the master list.  If an
            event has reached it's 'fire time' because of this, we fire off the event.
        
        Keyword arguments:
            None
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """
        for event in self.eventlist:
            event.passes = event.passes - 1
            if event.passes == 0:
                event.fire()
        

_eventcache = []

def _getEvent():
    """ A function to, theoretically, make event creation faster.  We take any 'fired' event, blank it out
        and add it to _eventcache.  When we need to create a new event we call this function which either returns
        an already created, but blank, event.  Or it creates a new event and returns that if there aren't any 'empty'
        events to reutlize.
    
    Keyword arguments:
        None
        
    Return value:
        A blank _Event instance.
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    if len(_eventcache) > 0:
        return _eventcache.pop()
    else:
        return _Event()

class _Event:
    """_Event:           
        Arguments:
            None
            
        Public Methods:
            clear(self):
                Arguments: None
                Return Type: Nothing
                     Blanks out a _Event object instance, then adds it to the eventcache for reuse.
                     
            fire(self):
                Arguments: None
                Return Type: Nothing
                     Removes the event in question (self) from the master list and the list of events of the owner object
                     instance.  It then executes the event code and uses it's own clear() instance method to clear the
                     event and add it to eventcache for future reuse.
                    
    """
    def __init__(self):
        self.eventtype = None
        self.ownertype = None
        self.owner = None
        self.func = None
        self.arguments = None
        self.passes = 0

    def clear(self):
        """ This method blanks out the event information for itself (instance).  It then adds itself 
            to the _eventcache for future reuse.
        
        Keyword arguments:
            None
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """
        self.eventtype = None
        self.ownertype = None
        self.owner = None
        self.func = None
        self.arguments = None
        self.passes = 0
        _eventcache.append(self)

    def fire(self):
        """ The fire instance method removes itself from the main event list, as well as the owners event list.
            The events function is then executed and the event is blanked out and added to the _eventcache.
        
        Keyword arguments:
            None
            
        Return value:
            None
            
        Example:
            None
            
        Additional notes:
            None
            
        """
        self.owner.events.remove(self)
        allevents.eventlist.remove(self)
        self.func(self)
        self.clear()


allevents = _Queue()

def init():
    """ I honestly don't recall why this is in here.  Perhaps in the event we need anything to happen upon
        game startup for this module.  This may go away....  XXX
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    pass

def heartbeat():
    """ This module function is used as a 'cheater' to call the allevents.update().  Not 100% necessary
        so this may go away.  XXX
    
    Keyword arguments:
        None
        
    Return value:
        A blank _Event instance.
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    allevents.update()



# Below follows the init functions.  If a particular thing needs to have
# an event set when it's created, it should go inside the appropriate
# init below.

PULSE_PER_SECOND = 8
PULSE_PER_MINUTE = PULSE_PER_SECOND * 60

def init_events_socket(socket):
    """ A placeholder function for now.  This will hold any reoccuring events that need to happen to 
        every socket that is created.  It will be the "Default" events for sockets.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    pass
    
def init_events_server(server):
    """ A placeholder function for now.   This will contain all events that are default for the game
        itself.  Anything in here is applied to the server upon startup.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    pass

def init_events_area(area):
    """ A placeholder function for now.  This will hold any reoccuring events that need to happen to 
        every area that is created.  It will be the "Default" events for areas.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    pass

def init_events_room(room):
    """ A placeholder function for now.  This will hold any reoccuring events that need to happen to 
        every room object that is created.  It will be the "Default" events for rooms.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    pass

def init_events_exit(exit_):
    """ A placeholder function for now.  This will hold any reoccuring events that need to happen to 
        every exit object that is created.  It will be the "Default" events for exits.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    pass

def init_events_mobile(mobile):
    """ A placeholder function for now.  This will hold any reoccuring events that need to happen to 
        every mobile that is created.  It will be the "Default" events for all mobiles.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    pass

def init_events_player(player): 
    """ This will hold any reoccuring events that need to happen to every player that is 
        created.  These are "default" events for players.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    event = _getEvent()
    event.owner = player
    event.ownertype = 'player'
    event.eventtype = 'autosave'
    event.func = event_player_autosave
    event.passes = 5 * PULSE_PER_MINUTE
    allevents.add(event)
    
def init_events_object(object_):
    """ A placeholder function for now.  This will hold any reoccuring events that need to happen to 
        every object that is created.  It will be the "Default" events for objects.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    pass


# Below are the actual events.
# Some events, such as the tick event, will recreate themselves.  This is
# currently the easiest way to set reoccuring events.

def event_player_autosave(event):
    """ Reoccuring Event:
            This function is a reoccuring event for players.  This is the actual code of what
            happens for the event that is recalled.  This can be used as a good template for adding
            in additional reoccuring events.
    
    Keyword arguments:
        None
        
    Return value:
        None
        
    Example:
        None
        
    Additional notes:
        None
        
    """
    # This is the 'recreation' of the event.
    nextevent = _getEvent()
    nextevent.owner = event.owner
    nextevent.ownertype = 'player'
    nextevent.eventtype = 'autosave'
    nextevent.func = event_player_autosave
    nextevent.passes = 5 * PULSE_PER_MINUTE
    allevents.add(nextevent)
    
    # The actual "event" that happens.
    event.owner.save()
