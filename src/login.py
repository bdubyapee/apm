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
#
# Filename: login.py
# 
# File Description: Login system.


import os
import sys
import time
import random
import hashlib

import area
import comm
import helpsys
import races
import world
import player
import livingthing
import fileparser

class Login:
    def __init__(self, name = ''):
        self.interp = self.get_char_name
        self.name = name
        self.newchar = {}
        self.newstats = {}
        self.sock = None

    def clear(self):
        self.interp = self.get_char_name
        self.newchar = {}
        self.newstats = {}
        self.sock = None

    def greeting(self):
        self.sock.dispatch(helpsys.get_help('greet', server=True ))
        self.sock.dispatch('\n\rPlease choose a character name: ', trail=False)
                
    def get_char_name(self, inp):
        inp = inp.lower()
        if len(inp) < 3 or len(inp) > 15:
            self.sock.dispatch('Character names must be between 3 and 15 characters long.')
            self.sock.dispatch('Enter a character name: ', trail=False)
        elif len(inp.split()) > 1:
            self.sock.dispatch('Character names must only contain one word.')
            self.sock.dispatch('Enter an character name: ', trail=False)
        elif not inp.isalpha():
            self.sock.dispatch('Character names may only contain letters.')
            self.sock.dispatch('Enter an character name: ', trail=False)
        else:
            self.name = inp.lower()
            if os.path.exists('{0}/{1}'.format(world.playerDir, self.name)):
                maybeplayer = fileparser.flatFileParse('{0}/{1}'.format(world.playerDir, self.name))
                self.password = maybeplayer['password']
                self.lasttime = maybeplayer['lasttime']
                self.lasthost = maybeplayer['lasthost']
                self.sock.dispatch('Please enter your password: ', trail=False)
                self.interp = self.get_char_password
                self.sock.dont_echo_telnet()
            else:
                if world.allownewCharacters:
                    self.sock.dispatch('Is this a new character? ', trail=False)
                    self.interp = self.confirm_new_char
                else:
                    self.sock.dispatch("I'm sorry, we aren't allowing new characters at this time.\n\r")
                    self.sock.dispatch("Contact someemail@address.com for an invite!")
                    self.sock.close()
                                
    def get_char_password(self, inp):
        inp = inp.encode('utf-8')
        md5_object = hashlib.md5(inp)
        if md5_object.hexdigest() != self.password:
            self.sock.dispatch("\n\rI'm sorry, that isn't the correct password. Good bye.")
            self.sock.handle_close()
        else:
            self.sock.do_echo_telnet()
            for person in player.playerlist:
                if person.name == self.name:
                    self.sock.dispatch('\n\rYour character seems to be logged in already.  Reconnecting you.')
                    del(person.sock.owner)
                    person.sock.close()
                    del(person.sock)
                    testsock = self.sock
                    self.clear()
                    person.sock = testsock
                    person.sock.owner = person
                    person.sock.promptable = True
                    person.write = person.sock.dispatch
                    comm.wiznet('{0} reconnecting from link death.'.format(person.name))
                    return
            comm.wiznet("{0} logged into main menu.".format(self.name.capitalize()))
            self.sock.dispatch('')
            self.sock.dispatch('Welcome back {0}'.format(self.name.capitalize()))
            self.sock.dispatch('You last logged in on {0}'.format(self.lasttime))
            self.sock.dispatch('From this host: {0}'.format(self.lasthost))
            self.sock.dispatch('')
            self.lasttime = time.ctime()
            self.lasthost = self.sock.host.strip()
            self.main_menu()
            self.interp = self.main_menu_get_option
                        
    def confirm_new_char(self, inp):
        inp = inp.lower()
        if inp == 'y' or inp == 'yes':
            self.sock.dont_echo_telnet()
            self.sock.dispatch('Please choose a password for this character: ', trail=False)
            self.interp = self.confirm_new_password
        else:
            self.sock.dispatch('Calm down.  Take a deep breath.  Now, lets try this again shall we?')
            self.sock.dispatch('Enter a character name: ', trail=False)
            self.interp = self.get_char_name
                        
    def confirm_new_password(self, inp):
        self.sock.dispatch('')
        if len(inp) < 3 or len(inp) > 30:
            self.sock.dispatch('Passwords must be between 3 and 30 characters long.')
            self.sock.dispatch('Please choose a password for this character: ', trail=False)
        else:
            self.password = inp
            self.sock.dispatch('Please reenter your password to confirm: ', trail=False)
            self.interp = self.confirm_new_password_reenter
                        
    def confirm_new_password_reenter(self, inp):
        if inp != self.password:
            self.password = ''
            self.sock.dispatch('Passwords do not match.')
            self.sock.dispatch('Please choose a password for this character: ', trail=False)
            self.interp = self.confirm_new_password
        else:
            inp = inp.encode('utf-8')
            md5_object = hashlib.md5(inp)
            self.password = md5_object.hexdigest()
            self.sock.do_echo_telnet()
            self.show_races()
            self.sock.dispatch('Please choose a race: ', trail=False)
            self.interp = self.get_race
                        
    def main_menu(self):
        self.sock.dispatch('Welcome to APM')
        self.sock.dispatch('-=-=-=====-=-=-')
        self.sock.dispatch('1) Login your character')
        self.sock.dispatch('2) View the Message of the Day')
        self.sock.dispatch('L) Logout')
        self.sock.dispatch('D) Delete this character')
        self.sock.dispatch('')
        self.sock.dispatch('Please choose an option: ', trail=False)
                
    def main_menu_get_option(self, inp):
        inp = inp.lower()
        if inp == '1':
            self.interp = self.character_login
            self.interp('')
        elif inp == '2':
            self.sock.dispatch(helpsys.get_help('motd', server=True))
            self.sock.dispatch('')
            self.main_menu()
        elif inp == 'l':
            self.sock.dispatch('Thanks for playing.  We hope to see you again soon.')
            comm.wiznet("{0} disconnecting from APM.".format(self.sock.host))
            self.sock.handle_close()
        elif inp == 'd':
            self.sock.dispatch('Sorry to see you go.  Come again soon!')
            os.remove('{0}/{1}'.format(world.playerDir, self.name))
            self.sock.close()
        else:
            self.main_menu()
                        
    def character_login(self, inp):
        path = '{0}\{1}'.format(world.playerDir, self.name)
        if os.path.exists(path):
            newobject = player.Player(path)
            testsock = self.sock
            self.clear()
            newobject.sock = testsock
            newobject.sock.owner = newobject
            newobject.sock.promptable = True
            newobject.write = newobject.sock.dispatch
            newobject.write('')
            newobject.write(helpsys.get_help('motd', server=True))
            newobject.write('')
            comm.wiznet('{0} logging into APM.'.format(newobject.name.capitalize()))
            player.playerlist.append(newobject)
            newobject.logpath = '{0}\{1}'.format(world.logDir, newobject.name)
            comm.log(newobject.logpath, 'Logging in from: {0}'.format(newobject.sock.host))
            newobject.interp('look')
            newobject.lasttime = time.ctime()
            newobject.lasthost = newobject.sock.host
        else:
            self.sock.dispatch('There seems to be a problem loading your file!  Notify an admin.')
            self.main_menu()
            self.interp = self.main_menu_get_option
                        
    def show_races(self):
        self.sock.dispatch('\n\rCurrently available races of APM')
        self.sock.dispatch('')
        self.sock.dispatch('Good races: {0}'.format(', '.join(races.goodraces)))
        self.sock.dispatch('Neutral races: {0}'.format(', '.join(races.neutralraces)))
        self.sock.dispatch('Evil races: {0}'.format(', '.join(races.evilraces)))
        self.sock.dispatch('')
                        
    def get_race(self, inp):
        inp = inp.lower()
        if inp in list(races.racesdict.keys()):
            self.newchar['race'] = races.racebyname(inp)
            self.newchar['aid'] = int(time.time())
            self.sock.dispatch("Available genders are: male female")
            self.sock.dispatch('Please choose a gender: ', trail=False)
            self.interp = self.get_gender
        else:
            self.sock.dispatch('That is not a valid race.')
            self.show_races()
            self.sock.dispatch('Please choose a race: ', trail=False)

    def get_gender(self, inp):
        inp = inp.lower()
        if inp in livingthing.genders:
            self.newchar['gender'] = inp
            self.roll_aesthetics()
            self.show_aesthetics()
            self.sock.dispatch('Do you wish to keep these aesthetics?', trail=False)
            self.interp = self.get_roll_aesthetics
        else:
            self.sock.dispatch("That isn't a valid gender.")
            self.sock.dispatch("Available genders are: male female")
            self.sock.dispatch("Please choose a gender: ", trail=False)
        
    def roll_aesthetics(self):
        self.newchar['aesthetic'] = 'A sexy, sexy beast.'
        
    def show_aesthetics(self):
        self.sock.dispatch('Randomly chosen aesthetic:')
        self.sock.dispatch(self.newchar['aesthetic'])
        self.sock.dispatch('')
        
    def get_roll_aesthetics(self, inp):
        inp = inp.lower()
        if inp == 'y' or inp == 'yes':
            self.show_disciplines()
            self.sock.dispatch('Please choose a base discipline: ', trail=False)
            self.interp = self.get_discipline
        else:
            self.roll_aesthetics()
            self.show_aesthetics()
            self.sock.dispatch('Do you wish to keep these aesthetics? ', trial=False)
                        
    def show_disciplines(self):
        self.sock.dispatch('Current base disciplines of APM:')
        self.sock.dispatch('{0}'.format(', '.join(livingthing.disciplines)))
        self.sock.dispatch('')
        
    def get_discipline(self, inp):
        inp = inp.lower()
        if inp in livingthing.disciplines:
            self.newchar['discipline'] = inp
            self.roll_stats()
            self.show_stats()
            self.sock.dispatch('Are these statistics acceptable? ', trail=False)
            self.interp = self.get_roll_stats
        else:
            self.sock.dispatch('That is not a valid discipline.  Choose a discipline: ', trail=False)
            self.show_disciplines()
            
    def roll_stats(self):
        self.newstats['strength'] = random.randint(1, 100)
        self.newstats['intelligence'] = random.randint(1, 100)
        self.newstats['wisdom'] = random.randint(1, 100)
        self.newstats['agility'] = random.randint(1, 100)
        self.newstats['speed'] = random.randint(1, 100)
        self.newstats['charisma'] = random.randint(1, 100)
        self.newstats['luck'] = random.randint(1, 100)
        self.newstats['constitution'] = random.randint(1, 100)
        
    def show_stats(self):
        self.sock.dispatch('Randomly rolled statistics:')
        for item in self.newstats.keys():
            self.sock.dispatch('{0} {1}'.format(item.capitalize(), self.newstats[item]))
        self.sock.dispatch('')
                        
    def get_roll_stats(self, inp):
        inp = inp.lower()
        if inp == 'y' or inp == 'yes':
            self.sock.dispatch(helpsys.get_help('motd', server=True))
            self.sock.dispatch('')
            newplayer = player.Player()
            newplayer.filename = "{0}/{1}".format(world.playerDir, self.name)
            testsock = self.sock
            newplayer.name = self.name
            newplayer.password = self.password
            newplayer.capability.append('player')
            newplayer.lasttime = time.ctime()
            newplayer.lasthost = self.sock.host
            newplayer.race = self.newchar['race']
            newplayer.aid = self.newchar['aid']
            newplayer.gender = self.newchar['gender']
            newplayer.discipline = self.newchar['discipline']
            newplayer.aesthetic = self.newchar['aesthetic']
            newplayer.position = 'standing'
            newplayer.maximum_stat = self.newstats
            newplayer.current_stat = self.newstats
            self.clear()
            newplayer.sock = testsock
            newplayer.sock.owner = newplayer
            newplayer.prompt = '{papmMUD{g:{x '
            newplayer.sock.promptable = True
            newplayer.write = newplayer.sock.dispatch
            player.playerlist.append(newplayer)
            newroom = area.roomByVnum(101)
            newplayer.move(newroom)
            newplayer.alias['s'] = 'south'
            newplayer.alias['n'] = 'north'
            newplayer.alias['e'] = 'east'
            newplayer.alias['w'] = 'west'
            newplayer.alias['ne'] = 'northeast'
            newplayer.alias['nw'] = 'northwest'
            newplayer.alias['sw'] = 'southwest'
            newplayer.alias['se'] = 'southeast'
            newplayer.alias['l'] = 'look'
            newplayer.alias['page'] = 'beep'
            newplayer.interp('look')
            newplayer.save()
            comm.wiznet("{0} is a new character entering APM.".format(newplayer.name))
            del(self)
        else:
            self.roll_stats()
            self.show_stats()
            self.sock.dispatch('Are these statistics acceptable? ', trail=False)

