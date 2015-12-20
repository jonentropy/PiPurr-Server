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
import wiringpi2 as wiringpi

wiringpi.wiringPiSetup()

# Set up pins
PIN_RED = 0
PIN_GREEN = 2
PIN_BLUE = 3
LED_MAX = 100

wiringpi.softPwmCreate(PIN_RED,   0, LED_MAX)
wiringpi.softPwmCreate(PIN_GREEN, 0, LED_MAX)
wiringpi.softPwmCreate(PIN_BLUE,  0, LED_MAX)
wiringpi.softPwmWrite(PIN_RED,   0)
wiringpi.softPwmWrite(PIN_GREEN, 0)
wiringpi.softPwmWrite(PIN_BLUE,  0)

# LedBorg colours.
RED = (1,0,0)
YELLOW = (1,1,0)
GREEN = (0,1,0)
BLUE = (0,0,1)
MAGENTA = (1,0,1)
OFF = (0,0,0)
WHITE = (1,1,1)

#For LedBorg lights
def setColour(colour):
    wiringpi.softPwmWrite(PIN_RED,   int(colour[0]  * LED_MAX))
    wiringpi.softPwmWrite(PIN_GREEN, int(colour[1] * LED_MAX))
    wiringpi.softPwmWrite(PIN_BLUE,  int(colour[2]  * LED_MAX))
    
def flashColour(colour):
    setColour(colour)
    time.sleep(0.5)
    setColour(OFF)  
