#!/usr/bin/env python

#
# PiPurrServer.py - PiPurr server module.
#
#   Allows remote interaction with your cats.
#
#   Contains code from piborg.org
#
#	Tris Linnell
#		http://canthack.org

print "Initialising..."

from cv2 import *
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
from datetime import datetime
import time
import pygame
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#Constants
PORT_NUMBER = 8081

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

# LedBorg colours
RED = (1,0,0)
GREEN = (0,1,0)
BLUE = (0,0,1)
OFF = (0,0,0)

#For LedBorg lights
def writeColour(colour):
	colour = "%d%d%d" % (colour[0], colour[1], colour[2])
	LedBorg = open("/dev/ledborg", 'w')
	LedBorg.write(colour)
	LedBorg.close()
    
def flashColour(colour):
	writeColour(colour)
	time.sleep(0.5)
	writeColour(OFF)    

#HTTP Server class
class myHandler(BaseHTTPRequestHandler):	
	
	#Override logging function with our own
	def log_message(self, format, *args):
		Log(self.address_string() + " (" + str(self.client_address[0]) + ") " + format%args);
		
	#Handler for the GET requests, which is all we are handling...
	def do_GET(self):
		#Ignore favicon requests to keep logs clean
		if self.path == "/favicon.ico":
			pass

		#Only continue if the server is asking for a known URI. Send
		#403 Forbidden HTTP response otherwise.
		
		elif self.path == "/feed":
			#feed cats
			MotorOff()
			MoveStep(200); #will be specific to your motor
			MotorOff()
			self.send_response(200, "Fed OK");
			
			self.send_header("Content-type", "text/html")
			self.end_headers()
			
			self.wfile.write("<html><head><title>" + os.path.basename(__file__) + "</title></head>")
			self.wfile.write("<body><p>Fed OK!</p>")
			self.wfile.write("</body></html>")
			self.wfile.close()
			
			flashColour(BLUE);
		
		elif self.path == "/sound":
			#play sound
			pygame.mixer.music.load("sound.ogg")
			pygame.mixer.music.play()
			self.send_response(200, "Sound played OK");
			
			self.send_header("Content-type", "text/html")
			self.end_headers()
			
			self.wfile.write("<html><head><title>" + os.path.basename(__file__) + "</title></head>")
			self.wfile.write("<body><p>Sound played OK!</p>")
			self.wfile.write("</body></html>")
			self.wfile.close()
			
			flashColour(BLUE);
		
		elif "/cats.jpeg" in self.path:				
			try:	
				#Capture the image
				camera.release()
				camera.open(0)
			
				#Set image dimensions. v4l and your webcam must support this
				camera.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320);
				camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240);
			
				status, image = camera.read()
				
				text = datetime.now().strftime("%H:%M:%S %a %d %b")
				textcolour = (200, 200, 255)
	 		
				putText(image, text, (2,20), FONT_HERSHEY_PLAIN, 1.0, textcolour)
	
				if status:
					self.send_response(200)
					self.send_header("Content-type", "image/jpg")
					self.end_headers()
					st, buffger = imencode(".jpg", image)
					self.wfile.write(buffger.tostring())
					self.wfile.close()
					flashColour(GREEN)
				else:
					#Something went wrong while creating the image,
					#Send 500 Internal Server Error
					self.send_error(500, "Image capture failed")
					flashColour(RED)
	
			except IOError:
				self.send_error(404, "File Not Found: %s" % self.path)
				flashColour(RED)
				
		else:
			#Unknown URI
			self.send_error(403, "Forbidden")
			Log("Headers in forbidden request:")

			for line in self.headers:
				Log(line + ": " + self.headers.get(line))
				
			flashColour(RED)	

logging = False;

def Log(msg):
	toLog = '[' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '] ' + msg
	print toLog;
	if logging:
		LogFile.write(toLog + "\n")

writeColour(BLUE)
		
try:
	LogFile = open(os.path.basename(__file__) + ".log", "a")
	logging = True

except Exception, e:
	print "Logging disabled, %s" %e
		
try:		
	# shut feeder motor off
	MotorOff()
    
	#Open the cat cam
	camera = VideoCapture(0)

	#For sound playback
	pygame.init()
	
	#Create the web server to serve the cat pics
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	Log("Server started on port " + str(PORT_NUMBER))

	writeColour(OFF)
	
	while(True):
		server.handle_request()

except KeyboardInterrupt:
	Log("Shutting down...")
	LogFile.close()
	server.socket.close()
	MotorOff()
	GPIO.cleanup()
