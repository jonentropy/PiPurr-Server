#!/usr/bin/env python

#
# feeder.py - PiPurr cat feeder module for PiPurr-Server
#
#
#   Contains code from piborg.org
#
#   Tris Linnell
#       http://canthack.org

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Set which GPIO pins the drive outputs are connected to
# for feeder control (stepper motor)
DRIVE_1 = 4  # Black
DRIVE_2 = 18 # Green
DRIVE_3 = 8  # Red
DRIVE_4 = 7  # Blue

# Tell the system how to drive the stepper
sequence = [DRIVE_1, DRIVE_3, DRIVE_2, DRIVE_4] # Order for stepping (see data sheet for the stepper motor)
stepDelay = 0.006                               # Delay between steps

# Set all of the drive pins as output pins
GPIO.setup(DRIVE_1, GPIO.OUT)
GPIO.setup(DRIVE_2, GPIO.OUT)
GPIO.setup(DRIVE_3, GPIO.OUT)
GPIO.setup(DRIVE_4, GPIO.OUT)

# Function to set all drives off
def MotorOff():
    global step
    GPIO.output(DRIVE_1, GPIO.LOW)
    GPIO.output(DRIVE_2, GPIO.LOW)
    GPIO.output(DRIVE_3, GPIO.LOW)
    GPIO.output(DRIVE_4, GPIO.LOW)
    step = -1
    
# Function to perform a sequence of steps as fast as allowed
def MoveStep(count):
    global step

    # Choose direction based on sign (+/-)
    if count < 0:
        dir = -1
        count *= -1
    else:
        dir = 1

    # Loop through the steps
    while count > 0:
        # Set a starting position if this is the first move
        if step == -1:
            GPIO.output(DRIVE_4, GPIO.HIGH)
            step = 0
        else:
            step += dir

        # Wrap step when we reach the end of the sequence
        if step < 0:
            step = len(sequence) - 1
        elif step >= len(sequence):
            step = 0

        # For this step turn one of the drives off and another on
        if step < len(sequence):
            GPIO.output(sequence[step-2], GPIO.LOW)
            GPIO.output(sequence[step], GPIO.HIGH)
        time.sleep(stepDelay)
        count -= 1
    
def feed():
    MotorOff()
    MoveStep(-200) #will be specific to your motor
    MotorOff()
    
def shutdown():
    MotorOff()
    GPIO.cleanup()
    
# shut feeder motor off
MotorOff()
