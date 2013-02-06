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
#

from cv2 import *
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from datetime import datetime

PORT_NUMBER = 8081

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
			return
			
		try:
			#Open the cat cam
			camera = VideoCapture(0)
			
			#Set image dimensions. v4l and your webcam must support this
			#camera.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640);
			#camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480);

			#Capture the image
			status, image = camera.read()
			camera.release()

			text = datetime.now().strftime("%H:%M:%S %a %d")
			textcolour = (120, 120, 120)
 			putText(image, text, (2,20), FONT_HERSHEY_COMPLEX_SMALL, 1.0, textcolour)

			if status:
				#Save image to temp file ready to serve it
				imwrite("cats.jpeg",image)
			
				f = open(curdir + sep + 'cats.jpeg') 

				self.send_response(200)
				self.send_header('Content-type', 'image/jpg')
				self.end_headers()

				self.wfile.write(f.read())
				f.close()
				return
			else:
				#Something went wrong while creating the image,
				#Send 500 Internal Server Error
				self.send_error(500, 'Image capture failed')

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

logging = False;

def Log(msg):
	toLog = '[' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '] ' + msg
	print toLog;
	if logging:
		LogFile.write(toLog + '\n')
		
try:
	LogFile = open('CatCamServer.log', 'a')
	logging = True
except Exception, e:
	print 'Logging disabled, %s' %e
		
try:		
	#Web server to serve the cat pics
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	Log('Cat pic server started on port ' + str(PORT_NUMBER))

	while(True):
		server.handle_request()	

except KeyboardInterrupt:
	Log('Shutting down...')
	LogFile.close()
	server.socket.close()
