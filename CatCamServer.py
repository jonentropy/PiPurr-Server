#!/usr/bin/env python

#
# CatCamServer.py - A very simple webcam server in python
#	Requires OpenCV for webcam capture.
#	Saves the image whenever the request is made
#	for any filename. Intended to work with a simple
#	Android app that fetches the image.
#
#	Tris Linnell
#		http://canthack.org

from cv2 import *
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from datetime import datetime
import time

#Constants
PORT_NUMBER = 8081

RED = (1,0,0)
GREEN = (0,1,0)
BLUE = (0,0,1)
OFF = (0,0,0)

#For LedBorg lights
def writeColour(colour):
	colour = "%d%d%d" % (colour[0], colour[1], colour[2])
	LedBorg = open('/dev/ledborg', 'w')
	LedBorg.write(colour)
	LedBorg.close()
    
def flashColour(colour):
	writeColour(colour)
	time.sleep(0.5)
	writeColour(OFF)    

#HTTP Server class
class myHandler(BaseHTTPRequestHandler):	
	
	#Overload logging function with our own
	def log_message(self, format, *args):
		Log(self.address_string() + ' ' + format%args);
		
	#Handler for the GET requests, which is all we are handling...
	def do_GET(self):
		#Only continue if the server is asking for /cats.jpeg. Send
		#403 Forbidden HTTP response otherwise
		if self.path != '/cats.jpeg':
			self.send_error(403, 'Forbidden')
			flashColour(RED)
			return
			
		try:	
			#Capture the image
			camera.release()
			camera.open(0)
		
			#Set image dimensions. v4l and your webcam must support this
			camera.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320);
			camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240);
		
			status, image = camera.read()
			
			text = datetime.now().strftime("%H:%M:%S %a %d")
			textcolour = (100, 100, 120)
 		
			putText(image, text, (2,20), FONT_HERSHEY_COMPLEX_SMALL, 1.0, textcolour)

			if status:
				self.send_response(200)
				self.send_header('Content-type', 'image/jpg')
				self.end_headers()
				st, buffger = imencode('.jpg', image)
				self.wfile.write(buffger.tostring())
				flashColour(GREEN)
				return
			else:
				#Something went wrong while creating the image,
				#Send 500 Internal Server Error
				self.send_error(500, 'Image capture failed')
				flashColour(RED)

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
			flashColour(RED)

logging = False;

def Log(msg):
	toLog = '[' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '] ' + msg
	print toLog;
	if logging:
		LogFile.write(toLog + '\n')

writeColour(BLUE)
		
try:
	LogFile = open('CatCamServer.log', 'a')
	logging = True

except Exception, e:
	print 'Logging disabled, %s' %e
		
try:		
	#Open the cat cam
	camera = VideoCapture(0)

	#Create the web server to serve the cat pics
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	Log('Cat pic server started on port ' + str(PORT_NUMBER))

	writeColour(OFF)
	
	while(True):
		server.handle_request()

except KeyboardInterrupt:
	Log('Shutting down...')
	LogFile.close()
	server.socket.close()
