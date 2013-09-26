#!/usr/bin/env python

#
# ledborg.py - ledborg module for PiPurr-Server
#
#
#   Contains code from piborg.org
#
#   Tris Linnell
#       http://canthack.org

import time

# LedBorg colours
RED = (1,0,0)
GREEN = (0,1,0)
BLUE = (0,0,1)
OFF = (0,0,0)

#For LedBorg lights
def writeColour(colour):
    colour = "%d%d%d" % (colour[0], colour[1], colour[2])
    ledBorg = open("/dev/ledborg", 'w')
    ledBorg.write(colour)
    ledBorg.close()
    
def flashColour(colour):
    writeColour(colour)
    time.sleep(0.5)
    writeColour(OFF)  
