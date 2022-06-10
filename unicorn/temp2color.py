#!/usr/bin/env python3

import colorsys
import unicornhat as uh
import datetime
from sys import argv

# this script should take a command line value that represents
# a temperature in C and shows the color it would represent
script, temperature = argv

# some math here...
# needs 'if > 35 then 35' & 'if < 0 then 0'

temp = (100 - temperature) / 100    


