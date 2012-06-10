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

"""Filename: color.py
 
File Description: Contains code to add, or remove, ANSI color capabilities for end users
                  using telnet clients.  This will eventually become the 'wilderness' module for
                  providing an in-game colorized ASCII character map for players to move around in
                  between areas.
               
                  
Public variables:
    None


Public functions:
    colorize(string) : return string
    
    decolorize(string) : return string


Public classes:
    None


Private variables:
    _color_table : dictionary
        Contains a mapping of 'special symbols' that equate to ANSI codes.


Private functions:
    None


Private classes:
    None
    
"""


# Mapping to convert APM type symbols to ANSI codes to send to telnet clients.

_color_table = {'{x': '0;0m', # Clear back to white on black
                 '{*': '\x07', # Beep code
                 '{d': '0;30m', # Set foreground color to black
                 '{r': '0;31m', # Set foreground color to red
                 '{g': '0;32m', # Set foreground color to green
                 '{y': '0;33m', # Set foreground color to yellow
                 '{b': '0;34m', # Set foreground color to blue
                 '{p': '0;35m', # Set foreground color to magenta (purple)
                 '{c': '0;36m', # Set foreground color to cyan
                 '{w': '0;37m', # Set foreground color to white
                 '{D': '1;30m', # Set foreground color to bright black
                 '{R': '1;31m', # Set foreground color to bright red
                 '{G': '1;32m', # Set foreground color to bright green
                 '{Y': '1;33m', # Set foreground color to bright yellow
                 '{B': '1;34m', # Set foreground color to bright blue
                 '{P': '1;35m', # Set foreground color to bright magenta (purple)
                 '{C': '1;36m', # Set foreground color to bright cyan
                 '{W': '1;37m', # Set foreground color to bright white
                 '{X': '0;40m', # Set background color to black
                 '{br': '0;41m', # Set background color to red
                 '{bg': '0;42m', # Set background color to green
                 '{by': '0;43m', # Set background color to yellow
                 '{bb': '0;44m', # Set background color to blue
                 '{bp': '0;45m', # Set background color to magenta
                 '{bc': '0;46m', # Set background color to cyan
                 '{bw': '0;47m', # Set background color to white
                 '{bD': '1;40m', # Set background color to bright black
                 '{bR': '1;41m', # Set background color to bright red
                 '{Z': '1;42m', # Set background color to bright green
                 '{bY': '1;43m', # Set background color to bright yellow
                 '{bB': '1;44m', # Set background color to bright blue
                 '{bP': '1;45m', # Set background color to bright magenta (purple)
                 '{bC': '1;46m', # Set background color to bright cyan
                 '{bW': '1;47m'} # Set background color to bright white

def colorize(text):
    """ Accept a string, return a string with ANSI color codes embedded in place of special characters.
    
    Keyword arguments:
        text  --  a string type
        
    Return value:
        return -- a string type
        
    Example:
        input = "I am a {W test string{x"
        return value = "I am a 1;37m test string0;0m"
        
    Additional notes:
        Used to provide color codes(ANSI) to end user telnet terminals that indicate they want color text.
        
        See the color_table dictionary in the color.py file for the symbol to ANSI code conversions.
        
    """
    if '{' in text:
        for item, code in _color_table.items():
            text = text.replace(item, '\x1b[{0}'.format(code))
        return text
    else:
        return text


def decolorize(text):
    """ Accept a string, return a string with with any special color codes removed.
    
    Keyword arguments:
        text  --  a string type
        
    Return value:
        return -- a string type
        
    Example:
        input = "I am a {W test string{x"
        return value = "I am a test string"
        
    Additional notes:
        Used to remove color codes symbols from outgoing text for users who don't have color capable
        telnet terminals.
        
        See the color_table dictionary in the color.py file for the symbol to ANSI code conversions.
        
    """
    if '{' in text:
        for item in _color_table.keys():
            text = text.replace(item, '')
        return text
    else:
        return text
