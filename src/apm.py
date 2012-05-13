#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: apm.py
# 
# File Description: Main "startup" file for Another Python MUD (apm).
# 
# By: admin

import server
    
if __name__ == "__main__":
    game = server.Server()
    game.run()
