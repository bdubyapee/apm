#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: server.py
# 
# File Description: The main server module.
# 
# By: admin


import asyncore
import os
from socket import AF_INET, AF_INET6, SOCK_STREAM
import string
from telnetlib import IAC, DONT, DO, WONT, WILL, theNULL, ECHO, SGA
import time

import commands
import helpsys
import color
import area
import comm
import login
import races
import event
import world
import player

# This is outside the scope of the rest of this module so we have a good
# reference time to base our total startup time.  Used only in the server
# __init__ to determine startup time.
startup = time.time()

# This is the connection list.  It will be a list of connected socket objects.
connlist = []

# Assistant variables for removing certain characters from out input.
validchars = string.printable
validchars = validchars.replace('~', '')
validchars = validchars.replace('|', '')
validchars = validchars.replace(':', '')
validchars = validchars.replace(string.whitespace[1:], '')

# Variables containing telnet codes for Go-Ahead Suppression
SGARequest = IAC + WILL + SGA
SGAAcknowledge = IAC + DO + SGA
DOECHOTELNET = IAC + WONT + ECHO + theNULL
DONTECHOTELNET = IAC + WILL + ECHO + theNULL

class ConnSocket(asyncore.dispatcher):
    def __init__(self, connection, address):
        asyncore.dispatcher.__init__(self, connection)
        self.owner = None
        self.host = address[0]
        self.inbuf = ''
        self.outbuf = ''
        self.ansi = True
        self.promptable = False
        self.suppressgoahead = False
        self.events = []
        event.init_events_socket(self)

    def clear(self):
        self.owner = None
        self.host = None
        self.inbuf = ''
        self.outbuf = ''
        self.ansi = True
        self.promptable = False
        self.suppressgoahead = False
        self.events = []

    def do_echo_telnet(self):
        try:
            self.send(DOECHOTELNET)
        except:
            pass
        return

    def dont_echo_telnet(self):
        try:
            self.send(DONTECHOTELNET)
        except:
            pass
        return        
        
    def writable(self):
        if self.outbuf != '':
            return True
        return False

    def parse_input(self, text):
        # Below we decode the bytes input into a string, linux telnet sends a 255 line after each input.
        # We check for that below.  Kinda ugly, but not sure how to handle it otherwise.
        if text.startswith(b'\xff'):
            return ''
        text = text.decode("utf8")
        
        # Here we check if there has just been an enter pressed.
        if text == "\r\n":
            return text
    
        # Sift through the input and validate good alphanums using a comprehension.
        output = ''.join(char for char in text if char in validchars)
        
        output = output.lstrip()

        # Append an enter to the input.  Stupid bytes.
        if len(output) > 0:
            output = output + '\r\n'
        else:
            output = ''

        return output

    def handle_read(self):
        indata = self.recv(4096)

        # Clients usually send the Suppress-Go-Ahead on connection.  This
        # tests for the suggestion, and sends the "Go ahead and suppress it"
        # code.
        if indata == SGARequest:
            indata = ''
            if not self.suppressgoahead:
                self.send(SGAAcknowledge)
                self.suppressgoahead = True

        self.inbuf = '{0}{1}'.format(self.inbuf, self.parse_input(indata))
        
        if '\r\n' in self.inbuf:
            args, self.inbuf = self.inbuf.split('\r\n')
            self.owner.interp(args)

    def handle_write(self):
        try:
            self.send(self.outbuf.encode("utf8"))
            self.outbuf = ''
            if hasattr(self.owner, 'editing'):
                output = ">"
                self.send(output.encode("utf8"))
            elif self.promptable == True:
                if self.owner.oocflags['afk'] == True:
                    pretext = "{W[{RAFK{W]{x "
                else:
                    pretext = ""
                output = color.colorize('\n\r{}{} '.format(pretext, self.owner.prompt))
                self.send(output.encode("utf8"))
        except Exception as err:
            print("Error in handle_write:server.py - {0}".format(err))

    def handle_close(self):
        self.handle_write()
        connlist.remove(self)
        self.clear()
        self.close()

    def dispatch(self, msg, trail=True):
        if trail:
            msg = '{0}\n\r'.format(msg)
        if self.ansi:
            msg = color.colorize(msg)
        else:
            msg = color.decolorize(msg)
        self.outbuf = '{0}{1}'.format(self.outbuf, msg)


class Server(asyncore.dispatcher):
    done = False
    softboot = False
    
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.logpath = os.path.join(world.logDir, 'server')
        self.events = []
        # Uncomment the below line if you want IPV6, or if your host operating system
        # allows mapped IPV4->IPV6 nativly.  Windows 7 doesn't do this (probably
        # without some flag I'm not setting....... I know Linux works.
        # self.create_socket(AF_INET6, SOCK_STREAM)
        self.create_socket(AF_INET, SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', 4000))
        self.listen(5)
        helpsys.init()
        races.init()
        commands.init()
        event.init()
        area.init()
        event.init_events_server(self)
        print('APM is up and running in {0:,.3f} seconds.'.format(time.time() - startup))

    def run(self):
        currenttime = time.time
        while not Server.done:
            timedelta = currenttime() + 0.125
            asyncore.poll()
            event.heartbeat()
            timenow = currenttime()
            if timenow < timedelta:
                time.sleep(timedelta - timenow)
        if Server.softboot == False:
            for conn in connlist:
                conn.close()
        else:
            # Add in a "copyover" style soft reboot.
            # Save state, save players, save file descriptors to disk.
            # Restart Mud, reload file descriptors and load players.
            # XXX Implement this at some point.
            pass
        print('System shutdown successful.')

    def handle_accept(self):
        newconn = login.Login()
        connection, address = self.accept()
        sock = ConnSocket(connection, address)
        newconn.sock = sock
        newconn.sock.owner = newconn
        connlist.append(sock)
        newconn.greeting()
        comm.wiznet('Accepting connection from: {0}'.format(newconn.sock.host))
        return sock

