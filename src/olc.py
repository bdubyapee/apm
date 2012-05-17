#! usr/bin/env python
# 
#  APM - Another Python Mud
#  Copyright (C) 2012  bdubyapee (BWP)
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
# Filename: olc.py
# 
# File Description: OLC module.


import textwrap

class Editable:
    def __init__(self):
        # Fully Implement this.
        self.beingedited = False
        
    def doAttrib(self, command=None, args=None):
        commlist = {'string': doString,
                    'list': doList,
                    'intlist': dointList,
                    'dict': doDict,
                    'integer': doInteger,
                    'description': doDescription}
        
        if args == None or command == None:
            raise SyntaxError("Error occured in doAttrib:olc.py")
        
        commtype, commset = self.commands[command]
        
        try:
            commlist[commtype](self, command, args, commset)
        except:
            raise SyntaxError("A command failed.  doAttrib.olc.py")

def doString(theobject=None, thestring=None, value=None, inset=None):
    if theobject == None:
        raise SyntaxError("No object given to doString. doString:olc.py")
    elif thestring == None:
        raise SyntaxError("No name given to doString:olc.py")
    elif value == None:
        return getattr(theobject, "%s" % (thestring,))
    else:
        value = value.lower().strip()
        if len(value) > 0 and len(value) < 50:
            if inset != None and value not in inset:
                raise SyntaxError("I'm sorry, valid options are: {0}".format(inset))
            setattr(theobject, thestring, value)
        else:
            raise SyntaxError('Strings must be between 3 and 15 characters.')

def doList(theobject=None, thestring=None, value=None, inset=None):
    if theobject == None:
        raise SyntaxError('No object given to doList.')
    elif thestring == None:
        raise SyntaxError('No name given to doList.')
    elif value == None:
        return getattr(theobject, "{0}".format(thestring))
    else:
        value = value.lower().strip()
        if len(value) > 0 and len(value) < 30:
            if inset != None and value not in inset:
                raise SyntaxError("I'm sorry, valid options are: {0}".format(inset))
            theattrib = getattr(theobject, "{0}".format(thestring))
            if value in theattrib:
                theattrib.remove(value)
            else:
                theattrib.append(value)
                
def dointList(theobject=None, thestring=None, value=None, inset=None):
    if theobject == None:
        raise SyntaxError('No object given to doList.')
    elif thestring == None:
        raise SyntaxError('No name given to doList.')
    elif value == None:
        return getattr(theobject, "{0}".format(thestring))
    else:
        try:
            value = int(value)
        except:
            raise SyntaxError("I'm sorry, thats not an integer!")
        if inset != None and value not in inset:
            raise SyntaxError("I'm sorry, valid options are: {0}".format(inset))
        theattrib = getattr(theobject, "{0}".format(thestring))
        if value in theattrib:
            theattrib.remove(value)
        else:
            theattrib.append(value)

def doInteger(theobject=None, thestring=None, value=None, inset=None):
    if theobject == None:
        raise SyntaxError('No object given to doInteger.')
    elif thestring == None:
        raise SyntaxError('No name given to doInteger.')
    elif value == None:
        return getattr(theobject, "{0}".format(thestring))
    else:
        value = value.lower().strip()
        try:
            value = int(value)
        except:
            raise SyntaxError('That is not a number.')
        if inset != None and value not in inset:
            raise SyntaxError("I'm sorry, valid options are: {0}".format(inset))
        setattr(theobject, thestring, value)

def doDict(theobject=None, thestring=None, args=None, sets=None):
    key = args.split()[0]
    value = args.split()[1:]
    keyset, valueset = sets
    if theobject == None:
        raise SyntaxError('No object given to doDict.')
    elif thestring == None:
        raise SyntaxError('No name given to doDict.')
    elif key == None:
        theattrib = getattr(theobject, "{0}".format(thestring))
        return theattrib
    elif value == None:
        theattrib = getattr(theobject, "{0}".format(thestring))
        if key in list(theattrib.keys()):
            return theattrib[key]
        else:
            raise SyntaxError('Key not found in doDict.')
    else:
        theattrib = getattr(theobject, "{0}".format(thestring))
        if keyset != None and key not in keyset:
            raise SyntaxError('Key not in key set in doDict.')
        if valueset != None and value not in valueset:
            raise SyntaxError('Value {0} not in value set {1} in doDict.'.format(value, valueset))
        if 'delete' in value:
            del theattrib[key]
        else:
            theattrib[key] = value

def doDescription(theobject=None, thestring=None, value=None, set=None):
    if theobject == None:
        raise SyntaxError('No object give to doDescription.')
    elif thestring == None:
        raise SyntaxError('No name given to doDescription.')
    else:
        value = getattr(theobject.builder.building, thestring)
        theobject.builder.editing = Buffer(value)
        theobject.builder.editing_obj_name = '{0}'.format(thestring)
        theobject.builder.write(theobject.builder.editing.display())


class Buffer:
    def __init__(self, oldbuffer=None):
        if oldbuffer != None:
            self.lines = oldbuffer.split('\n')
        else:
            self.lines = []
        self.commands = {'.ld': self.delete_line,
                         '.lr': self.replace_line,
                         '.li': self.insert_line,
                         '.si': self.space_insert,
                         '.d': self.delete_word,
                         '.r': self.replace_word,
                         '.c': self.clear,
                         '.s': self.display,
                         '.sc': self.spellcheck,
                         '.f': self.formattext,
                         '.h': self.helpfunc,
                          '@': self.done}

    def spellcheck(self, args):
        return False

    def add(self, args):
        self.lines.append(args)
        return False

    def delete_line(self, args):
        try:
            linenumber = int(args.split()[0])
            self.lines.pop(linenumber)
        except:
            return "There has been an error processing your request"
        return False
    
    def insert_line(self, args):
        try:
            data = args.split()
            linenumber = int(data[0])
            text = ' '.join(data[1:])
            self.lines.insert(linenumber, text)
        except:
            return "There has been an error processing your request"
        return False
    
    def space_insert(self, args):
        try:
            data = args.split()
            linenumber = int(data[0])
            amount = int(data[1])
            self.lines[linenumber] = (' ' * amount) + self.lines[linenumber]
        except:
            return "There was an error processing your request"
        return False

    def replace_line(self, args):
        try:
            data = args.split()
            linenumber = int(data[0])
            text = ' '.join(data[1:])
            self.lines[linenumber] = text
        except:
            return "There was an error processing your request."
        return False

    def replace_word(self, args):
        try:
            data = args.split()
            linenumber = int(data[0])
            old = data[1]
            new = data[2]
            if old in self.lines[linenumber]:
                self.lines[linenumber] = self.lines[linenumber].replace(old, new)
        except:
            return "There was an error processing your request."
        return False

    def delete_word(self, args):
        try:
            data = args.split()
            linenumber = int(data[0])
            text = ' '.join(data[1:])
            if text in self.lines[linenumber]:
                self.lines[linenumber] = self.lines[linenumber].replace(text, '')
        except:
            return "There was an error processing your request."
        return False

    def clear(self, args):
        self.lines = []
        return False

    def done(self, args):
        self.lines = '\n'.join(self.lines)
        return True

    def display(self, args=None):
        output = []
        output.append("-=-=-=-=-=-=-=-=-= Entering Edit Mode =-=-=-=-=-=-=-=-=-".center(76))
        output.append("Type .h on a new line for help, or @ to exit.".center(76))
        output.append("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-".center(76))
        for number, line in enumerate(self.lines):
            output.append('{0}: {1}'.format(number, line))
        return '\n\r'.join(output)

    def helpfunc(self, args):
        output = ".ld #             Delete the given line number.\n\r"\
                  ".lr # text        Replace the given line number with text.\n\r"\
                  ".li # text        Inserts the text above line number #\n\r"\
                  ".si # amount      Inserts the amount of spaces on line #\n\r"\
                  ".d # the text     Delete 'the text' on line number #.\n\r"\
                  ".r # old new      Replace old text with new text.\n\r"\
                  ".c                Clear the entire buffer.  (Beware!).\n\r"\
                  ".sc word          Spellcheck the given word (Broken).\n\r"\
                  ".s                Show the string so far.\n\r"\
                  ".f                Format the text to 80 characters wide.\n\r"\
                  "                  (Do not do this on preformatted text)\n\r"\
                  ".h                This help screen.\n\r"\
                  "@                 Exit this editor.\n\r"
        return output

    def formattext(self, args):
        formatter = textwrap.TextWrapper(width=76)
        self.lines = formatter.wrap(' '.join(self.lines))
        return False
