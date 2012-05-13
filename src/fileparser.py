#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: fileparse.py
# 
# File Description: File to handle flatfile parsing, loading and writing.
# 
# By: admin


def flatFileParse(thepath):
    with open(thepath, 'r') as thefile:
        data = thefile.read()
    
    data = [item.strip() for item in data.split('~') if item.strip() != '']
    dictinfo = {}
    for thing in data:
        first = thing.index('|')
        dictinfo[thing[:first].strip()] = thing[first + 1:].strip()
    return dictinfo

def listWrite(thelist):
    output = []
    for item in thelist:
        output.append(str(item))
    return ', '.join(output)
        
def textRead(thetext):
    return thetext.strip()
        
def listRead(thelist):
    return [i.strip() for i in thelist.split(',') if len(i.strip()) > 0]

def dictWrite(thedict):
    retvalue = []
    for key in list(thedict.keys()):
        if type(thedict[key]) == type([]):
            thedict[key] = ' '.join(thedict[key])
            if len(thedict[key]) <= 0:
                thedict.pop(key)
                return
        retvalue.append('{0} : {1}'.format(key, thedict[key]))
    return ','.join(retvalue)

def dictRead(thedict):
    retvalue = {}
    items = thedict.split(',')
    for item in items:
        if item != '':
            retvalue[item.split(':')[0].strip()] = item.split(':')[1].strip()
    return retvalue

def boolRead(thedict):
    if thedict.lower() == 'true':
        return True
    else:
        return False

def boolWrite(thedict):
    if thedict == True:
        return 'true'
    else:
        return 'false'
