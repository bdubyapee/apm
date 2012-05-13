#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: event.py
# 
# File Description: Module to handle event queues.
# 
# By: admin

import sys
import time

import player


class Queue:
    def __init__(self):
        self.eventlist = []

    def add(self, event):
        self.eventlist.append(event)
        event.owner.events.append(event)

    def remove(self, event):
        event.owner.events.remove(event)
        self.eventlist.remove(event)

    def removePlayer(self, player):
        for item in player.events:
            self.remove(item)

    def update(self):
        for event in self.eventlist:
            event.passes = event.passes - 1
            if event.passes == 0:
                event.fire()
        

eventcache = []

def getEvent():
    if len(eventcache) > 0:
        return eventcache.pop()
    else:
        return Event()

class Event:
    def __init__(self):
        self.eventtype = None
        self.ownertype = None
        self.owner = None
        self.func = None
        self.arguments = None
        self.passes = 0

    def clear(self):
        self.eventtype = None
        self.ownertype = None
        self.owner = None
        self.func = None
        self.arguments = None
        self.passes = 0
        eventcache.append(self)

    def fire(self):
        self.owner.events.remove(self)
        allevents.eventlist.remove(self)
        self.func(self)
        self.clear()


allevents = Queue()

def init():
    pass

def heartbeat():
    allevents.update()



# Below follows the init functions.  If a particular thing needs to have
# an event set when it's created, it should go inside the appropriate
# init below.

PULSE_PER_SECOND = 8
PULSE_PER_MINUTE = PULSE_PER_SECOND * 60

def init_events_socket(socket):
    pass
    
def init_events_server(server):
    pass

def init_events_area(area):
    pass

def init_events_room(room):
    pass

def init_events_exit(exit_):
    pass

def init_events_mobile(mobile):
    pass

def init_events_player(player): 
    event = getEvent()
    event.owner = player
    event.ownertype = 'player'
    event.eventtype = 'autosave'
    event.func = event_player_autosave
    event.passes = 5 * PULSE_PER_MINUTE
    allevents.add(event)
    
def init_events_object(object_):
    pass


# Below are the actual events.
# Some events, such as the tick event, will recreate themselves.  This is
# currently the easiest way to set reoccuring events.

def event_player_autosave(event):
    nextevent = getEvent()
    nextevent.owner = event.owner
    nextevent.ownertype = 'player'
    nextevent.eventtype = 'autosave'
    nextevent.func = event_player_autosave
    nextevent.passes = 5 * PULSE_PER_MINUTE
    allevents.add(nextevent)
    
    event.owner.save()
