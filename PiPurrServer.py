#!/usr/bin/env python

#
# PiPurrServer.py - PiPurr server module.
#
#   Allows remote interaction with your cats.
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

#Constants
PORT_NUMBER = 8081

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
	
	#Overload logging function with our own
	def log_message(self, format, *args):
		Log(self.address_string() + " (" + str(self.client_address[0]) + ") " + format%args);
		
	#Handler for the GET requests, which is all we are handling...
	def do_GET(self):
		#Ignore favicon requests to keep logs clean
		if self.path == "/favicon.ico":
			pass

		#Only continue if the server is asking for a known URI. Send
		#403 Forbidden HTTP response otherwise.
		
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
		
		elif self.path == "/cats.jpeg":				
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
