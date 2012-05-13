#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: world.py
# 
# File Description: Contains configuration data
#
# By: admin

import os

# Directory Configuration values
homeDir = 'c:\\apm'
dataDir = os.path.join(homeDir, 'data')
logDir = os.path.join(dataDir, 'log')
helpDir = os.path.join(dataDir, 'help')
playerDir = os.path.join(dataDir, 'players')
raceDir = os.path.join(dataDir, 'races')
areaDir = os.path.join(dataDir, 'areas')
commandDir = os.path.join(dataDir, 'commands')


# Generic Configurables
allownewCharacters = True
