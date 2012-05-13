#! usr/bin/env python
# Project: Another Python MUD (apm)
# Filename: math.py
# 
# File Description: Math functions that may be handy to have available.
# 
# By: admin

import random
from functools import reduce

def dice(num, sides):
    def accumulate(x, y, s=sides): return x + random.randrange(s)
    return reduce(accumulate, list(list(range(num+1)))) + num