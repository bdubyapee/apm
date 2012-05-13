#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: color.py
# 
# File Description: Currently is the color code place holder.  Will turn into the wilderness file.
# 
# By: admin


# Color utility functions.
# Don't forget to rewrite this to do 1/0;fore;backm at somepoint.
color_table = {'{x': '0;0m', # Clear back to white on black
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
    if '{' in text:
        for item, code in color_table.items():
            text = text.replace(item, '\x1b[{0}'.format(code))
        return text
    else:
        return text
    
def decolorize(text):
    if '{' in text:
        for item in color_table.keys():
            text = text.replace(item, '')
        return text
    else:
        return text
