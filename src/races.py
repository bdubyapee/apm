#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: races.py
# 
# File Description: Module to deal with races.
# 
# By: admin

import os
import glob

import olc
from fileparser import flatFileParse, listWrite, listRead, textRead
from fileparser import dictWrite, dictRead, boolRead, boolWrite
import world


sizelist = ('tiny', 'small', 'medium', 'large', 'huge')
alignment = ('lawful good', 'lawful neutral', 'lawful evil',
             'neutral good', 'neutral', 'neutral evil',
             'chaotic good', 'chaotic neutral', 'chaotic evil')
bodypartslist = ('head', 'face', 'hand', 'leg', 'foot', 'nose', 'ear', 'scalp', 'torso', 'finger',
                 'toe', 'entrails', 'wing', 'tail', 'snout', 'shell', 'antenna', 'paw',
                 'fin', 'scale', 'rattle', 'tongue', 'eye', 'skull', 'arm', 'bone', 'pelt', 'heart',
                 'liver', 'stomach', 'kidney', 'lung', 'gills', 'claw', 'beak', 'feather',
                 'whisker', 'tooth', 'tusk', 'horn', 'hoof', 'hide', 'tentacle', 'mane', 'mandible',
                 'thorax')
wearlocationslist = ('head', 'face', 'eyes', 'neck', 'left arm', 'right arm',
                     'right forearm', 'left forearm', 'finger', 'left hand',
                     'right hand', 'torso', 'back', 'waist', 'left leg',
                     'right leg', 'left shin', 'right shin', 'left foot',
                     'right foot', 'left shoulder', 'right shoulder',
                     'upper right arm', 'upper left arm', 
                     'upper right hand', 'upper left hand', 'upper right forearm',
                     'upper left forearm', 'horns', 'floating nearby', 'tail')

height_list_values = [number for number in range(12)]
ac_and_resistance_values = [number for number in range(-50, 51)]
start_locationlist = {'drowhome': 101,  'stormhaven': 101, 'whitestone keep':101}
special_skillslist = ['drow', 'elven', 'high elven', 'common']

class oneRace(olc.Editable):
    def __init__(self, path):
        olc.Editable.__init__(self)
        self.path = path
        self.builder = None
        self.name = ''
        self.description = ''
        self.alignment = []
        self.playable = 'false'
        self.descriptive = ''
        self.size = ''
        self.heightfeet = 0
        self.heightinches = 0
        self.undead = 'false'
        self.weight = 0
        self.ageminimum = 0
        self.agemaximum = 0
        self.baslashing = 0
        self.babashing = 0
        self.bapiercing = 0
        self.balashing = 0
        self.brfire = 0
        self.brice = 0
        self.brlightning = 0
        self.brearth = 0
        self.brdisease = 0
        self.brpoison = 0
        self.brmagic = 0
        self.brholy = 0
        self.brmental = 0
        self.brphysical = 0
        self.wearlocations = []
        self.bodyparts = []
        self.skin = []
        self.eyes = []
        self.hair = []
        self.speed = 0
        self.agility = 0
        self.strength = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        self.luck = 0
        self.constitution = 0
        self.start_location = {}
        self.special_skills = {}
        self.commands = {'name': ('string', None),
                         'description': ('description', None),
                         'alignment': ('list', alignment),
                         'playable': ('string', ['true', 'false']),
                         'descriptive': ('string', None),
                         'size': ('string', sizelist),
                         'heightfeet': ('integer', height_list_values),
                         'heightinches': ('integer', height_list_values),
                         'undead': ('string', ['true', 'false']),
                         'weight': ('integer', None),
                         'ageminimum': ('integer', None),
                         'agemaximum': ('integer', None),
                         'baslashing': ('integer', ac_and_resistance_values),
                         'babashing': ('integer', ac_and_resistance_values),
                         'bapiercing': ('integer', ac_and_resistance_values),
                         'balashing': ('integer', ac_and_resistance_values),
                         'brfire': ('integer', ac_and_resistance_values),
                         'brice': ('integer', ac_and_resistance_values),
                         'brlightning': ('integer', ac_and_resistance_values),
                         'brearth': ('integer', ac_and_resistance_values),
                         'brdisease': ('integer', ac_and_resistance_values),
                         'brpoison': ('integer', ac_and_resistance_values),
                         'brmagic': ('integer', ac_and_resistance_values),
                         'brholy': ('integer', ac_and_resistance_values),
                         'brmental': ('integer', ac_and_resistance_values),
                         'brphysical': ('integer', ac_and_resistance_values),
                         'wearlocations': ('list', wearlocationslist),
                         'bodyparts': ('list', bodypartslist),
                         'skin': ('list', None),
                         'eyes': ('list', None),
                         'hair': ('list', None),
                         'speed': ('integer', None),
                         'agility': ('integer', None),
                         'strength': ('integer', None),
                         'intelligence': ('integer', None),
                         'wisdom': ('integer', None),
                         'charisma': ('integer', None),
                         'luck': ('integer', None),
                         'constitution': ('integer', None),
                         'start_location': ('dict', (list(start_locationlist.keys()),
                                                     list(start_locationlist.values()))),
                         'special_skills': ('list', special_skillslist)}
        if os.path.exists(path):
            self.load()

    def load(self):
        dictinfo = flatFileParse(self.path)
        self.name = dictinfo['name']
        self.description = dictinfo['description']
        self.alignment = listRead(dictinfo['alignment'])
        self.playable = dictinfo['playable']
        self.descriptive = dictinfo['descriptive']
        self.size = dictinfo['size']
        self.heightfeet = int(dictinfo['heightfeet'])
        self.heightinches = int(dictinfo['heightinches'])
        self.undead = dictinfo['undead']
        self.weight = int(dictinfo['weight'])
        self.ageminimum = int(dictinfo['ageminimum'])
        self.agemaximum = int(dictinfo['agemaximum'])
        self.baslashing = int(dictinfo['baslashing'])
        self.babashing = int(dictinfo['babashing'])
        self.bapiercing = int(dictinfo['bapiercing'])
        self.balashing = int(dictinfo['balashing'])
        self.brfire = int(dictinfo['brfire'])
        self.brice = int(dictinfo['brice'])
        self.brlightning = int(dictinfo['brlightning'])
        self.brearth = int(dictinfo['brearth'])
        self.brdisease = int(dictinfo['brdisease'])
        self.brpoison = int(dictinfo['brpoison'])
        self.brmagic = int(dictinfo['brmagic'])
        self.brholy = int(dictinfo['brholy'])
        self.brmental = int(dictinfo['brmental'])
        self.brphysical = int(dictinfo['brphysical'])
        self.wearlocations = listRead(dictinfo['wearlocations'])
        self.bodyparts = listRead(dictinfo['bodyparts'])
        self.skin = listRead(dictinfo['skin'])
        self.eyes = listRead(dictinfo['eyes'])
        self.hair = listRead(dictinfo['hair'])
        self.speed = dictinfo['speed']
        self.speed = int(self.speed)
        self.agility = dictinfo['agility']
        self.agility = int(self.agility)
        self.strength = dictinfo['strength']
        self.strength = int(self.strength)
        self.intelligence = dictinfo['intelligence']
        self.intelligence = int(self.intelligence)
        self.wisdom = dictinfo['wisdom']
        self.wisdom = int(self.wisdom)
        self.charisma = dictinfo['charisma']
        self.charisma = int(self.charisma)
        self.luck = dictinfo['luck']
        self.luck = int(self.luck)
        self.constitution = dictinfo['constitution']
        self.constitution = int(self.constitution)
        self.start_location = dictRead(dictinfo['start_location'])
        self.special_skills = dictRead(dictinfo['special_skills'])

    def save(self):
        with open(self.path, 'w') as thefile:
            thefile.write('name | {0}~\n'.format(self.name))
            thefile.write('description | {0}~\n'.format(self.description))
            thefile.write('alignment | {0}~\n'.format(listWrite(self.alignment)))
            thefile.write('playable | {0}~\n'.format(self.playable))
            thefile.write('descriptive | {0}~\n'.format(self.descriptive))
            thefile.write('size | {0}~\n'.format(self.size))
            thefile.write('heightfeet | {0}~\n'.format(self.heightfeet))
            thefile.write('heightinches | {0}~\n'.format(self.heightinches))
            thefile.write('undead | {0}~\n'.format(self.undead))
            thefile.write('weight | {0}~\n'.format(self.weight))
            thefile.write('ageminimum | {0}~\n'.format(self.ageminimum))
            thefile.write('agemaximum | {0}~\n'.format(self.agemaximum))
            thefile.write('baslashing | {0}~\n'.format(self.baslashing))
            thefile.write('babashing | {0}~\n'.format(self.babashing))
            thefile.write('bapiercing | {0}~\n'.format(self.bapiercing))
            thefile.write('balashing | {0}~\n'.format(self.balashing))
            thefile.write('brfire | {0}~\n'.format(self.brfire))
            thefile.write('brice | {0}~\n'.format(self.brice))
            thefile.write('brlightning | {0}~\n'.format(self.brlightning))
            thefile.write('brearth | {0}~\n'.format(self.brearth))
            thefile.write('brdisease | {0}~\n'.format(self.brdisease))
            thefile.write('brpoison | {0}~\n'.format(self.brpoison))
            thefile.write('brmagic | {0}~\n'.format(self.brmagic))
            thefile.write('brholy | {0}~\n'.format(self.brholy))
            thefile.write('brmental | {0}~\n'.format(self.brmental))
            thefile.write('brphysical | {0}~\n'.format(self.brphysical))
            thefile.write('wearlocations | {0}~\n'.format(listWrite(self.wearlocations)))
            thefile.write('bodyparts | {0}~\n'.format(listWrite(self.bodyparts)))
            thefile.write('skin | {0}~\n'.format(listWrite(self.skin)))
            thefile.write('eyes | {0}~\n'.format(listWrite(self.eyes)))
            thefile.write('hair | {0}~\n'.format(listWrite(self.hair)))
            thefile.write('speed | {0}~\n'.format(self.speed))
            thefile.write('agility | {0}~\n'.format(self.agility))
            thefile.write('strength | {0}~\n'.format(self.strength))
            thefile.write('intelligence | {0}~\n'.format(self.intelligence))
            thefile.write('wisdom | {0}~\n'.format(self.wisdom))
            thefile.write('charisma | {0}~\n'.format(self.charisma))
            thefile.write('luck | {0}~\n'.format(self.luck))
            thefile.write('constitution | {0}~\n'.format(self.constitution))
            thefile.write('start_location | {0}~\n'.format(dictWrite(self.start_location)))
            thefile.write('special_skills | {0}~\n'.format(dictWrite(self.special_skills)))

    def display(self):
        retvalue = "Name: {0}\n\r"\
                   "Alignment: {1}\n\r"\
                   "Playable: {2}\n\r"\
                   "Descriptive: {3}\n\r"\
                   "Size: {4}\n\r"\
                   "HeightFeet: {5}\n\r"\
                   "HeightInches: {6}\n\r"\
                   "Undead: {7}\n\r"\
                   "Weight: {8}\n\r"\
                   "AgeMinimum: {9}\n\r"\
                   "AgeMaximum: {10}\n\r"\
                   "BaSlashing: {11}\n\r"\
                   "BaBashing: {12}\n\r"\
                   "BaPiercing: {13}\n\r"\
                   "BaLashing: {14}\n\r"\
                   "BrFire: {15}\n\r"\
                   "BrIce: {16}\n\r"\
                   "BrLightning: {17}\n\r"\
                   "BrEarth: {18}\n\r"\
                   "BrDisease: {19}\n\r"\
                   "BrPoison: {20}\n\r"\
                   "BrMagic: {21}\n\r"\
                   "BrHoly: {22}\n\r"\
                   "BrMental: {23}\n\r"\
                   "BrPhysical: {24}\n\r"\
                   "Skin: {25}\n\r"\
                   "Eyes: {26}\n\r"\
                   "Hair: {27}\n\r"\
                   "Speed: {28}\n\r"\
                   "Agility: {29}\n\r"\
                   "Strength: {30}\n\r"\
                   "Intelligence: {31}\n\r"\
                   "Wisdom: {32}\n\r"\
                   "Charisma: {33}\n\r"\
                   "Luck: {34}\n\r"\
                   "Constitution: {35}\n\r"\
                   "WearLocations: {36}\n\r"\
                   "BodyParts: {37}\n\r"\
                   "Start Locations: {38}\n\r"\
                   "Special Skills: {39}\n\r"\
                   "Description:\n\r"\
                   "{40}...\n\r".format(
                      self.name.capitalize(), self.alignment,
                      self.playable, self.descriptive,
                      self.size, self.heightfeet, self.heightinches,
                      self.undead,
                      self.weight, self.ageminimum, self.agemaximum,
                      self.baslashing, self.babashing, self.bapiercing, self.balashing,
                      self.brfire, self.brice, self.brlightning,
                      self.brearth, self.brdisease, self.brpoison,
                      self.brmagic, self.brholy, self.brmental,
                      self.brphysical,
                      self.skin, self.eyes, self.hair, self.speed,
                      self.agility, self.strength,
                      self.intelligence, self.wisdom, self.charisma,
                      self.luck, self.constitution,
                      self.wearlocations, self.bodyparts,
                      self.start_location,
                      self.special_skills,
                      self.description[:180])
        return retvalue
   
goodraces = []
neutralraces = []
evilraces = []
racesdict = {}

def init():
    racepaths = glob.glob(os.path.join(world.raceDir, '*'))
    for racepath in racepaths:
        therace = oneRace(racepath)
        addtolist(therace)

def reload():
    racesdict = {}
    goodraces = []
    neutralraces = []
    evilraces = []
    init()

def addtolist(race):
    racesdict[race.name.lower()] = race
    alignments = {'lawful good' : goodraces,
                  'neutral good' : goodraces,
                  'chaotic good' : goodraces,
                  'lawful neutral' : neutralraces,
                  'neutral' : neutralraces,
                  'chaotic neutral' : neutralraces,
                  'lawful evil' : evilraces,
                  'neutral evil' : evilraces,
                  'chaotic evil' : evilraces}
    if race.alignment[0].lower() in alignments and race.playable == 'true':
        alignments[race.alignment[0]].append(race.name.lower())

def racebyname(name):
    if name in racesdict:
        return racesdict[name]
    else:
        raise SyntaxError('Thats not a race I recognize.')

