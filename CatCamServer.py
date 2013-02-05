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

PORT_NUMBER = 8081

#HTTP Server class
class myHandler(BaseHTTPRequestHandler):	

	#Handler for the GET requests, which is all we are handling...
	def do_GET(self):
		try:
			#Open the cat cam
			camera = VideoCapture(0)

			#Set image dimensions. v4l and your webcam must support this
			camera.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640);
			camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480);

			#Capture the image
			status, image = camera.read()
			camera.release()

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
				self.send_error(404, 'Image capture failed')


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Web server to serve the cat pics
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Cat pic server started on port' , PORT_NUMBER

	while(True):
		server.handle_request()	

except KeyboardInterrupt:
	print '\nShutting down...'
	server.socket.close()

