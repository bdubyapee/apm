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
# Filename: world.py
# 
# File Description: Contains configuration data.


import os

# Generic configuration values.


# homeDir is the root path, it should contain 'data' and 'src' directories.
homeDir = 'c:\\Users\\bwp\\apm'

# dataDir is the root path to all of the data files.  logs, help files, areas etc.  See below.
dataDir = os.path.join(homeDir, 'data')

# Absolute path to the log file directory.  We keep player log files and APM log files here.
logDir = os.path.join(dataDir, 'log')

# Absolute path to the 'in-game' help files.
helpDir = os.path.join(dataDir, 'help')

# Absolute path to the player files.
playerDir = os.path.join(dataDir, 'players')

# Absolute path to the race definition files.
raceDir = os.path.join(dataDir, 'races')

# Absolute path to the area files.
areaDir = os.path.join(dataDir, 'areas')

# Absolute path to the command files.  
commandDir = os.path.join(dataDir, 'commands')


# Generic Configurables
allownewCharacters = True
