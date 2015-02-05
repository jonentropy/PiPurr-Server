#!/usr/bin/env python

#
# PiPurrServer.py - PiPurr server module.
#
#   Allows remote interaction with your cats.
#
#   Contains code from piborg.org
#
#   Tris Linnell
#       http://canthack.org

if __name__ == "__main__":
    print "Initialising..."

import cv2
import cv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
from datetime import datetime
import time
import pygame
import feeder
import ledborg

PORT_NUMBER = 8081  

logging = False

#HTTP Server class
class PiPurrServer(BaseHTTPRequestHandler):    
    
    #Override logging function with our own
    def log_message(self, format, *args):
        log(self.address_string() + " (" + str(self.client_address[0]) + ") " + format%args)
        
    #Handler for the GET requests, which is all we are handling...
    def do_GET(self):
        #Ignore favicon requests to keep logs clean
        if "/favicon.ico" in self.path:
            pass

        #Only continue if the server is asking for a known URI. Send
        #403 Forbidden HTTP response otherwise.
        
        elif "/feed" in self.path:
            #feed cats
            feeder.feed()
            self.send_response(200, "Fed OK")
            
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            self.wfile.write("<!DOCTYPE html>")
            self.wfile.write("<html><head><title>" + os.path.basename(__file__) + "</title></head>")
            self.wfile.write("<body><p>Fed OK!</p>")
            self.wfile.write("</body></html>")
            self.wfile.close()
            
            ledborg.flashColour(ledborg.YELLOW)
        
        elif "/sound" in self.path:
            #play sound
            pygame.mixer.music.load("sound.ogg")
            pygame.mixer.music.play()
            self.send_response(200, "Sound played OK")
            
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            self.wfile.write("<!DOCTYPE html>")
            self.wfile.write("<html><head><title>" + os.path.basename(__file__) + "</title></head>")
            self.wfile.write("<body><p>Sound played OK!</p>")
            self.wfile.write("</body></html>")
            self.wfile.close()
            
            ledborg.flashColour(ledborg.BLUE)
        
        elif "/cats.jpeg" in self.path:             
            try:    
                #Capture the image
                camera.release()
                camera.open(0)
            
                #Set image dimensions. v4l and your webcam must support this
                camera.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320)
                camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
            
                status, image = camera.read()
                
                text = "PiPurr " + datetime.now().strftime("%H:%M:%S %a %d %b")
                textcolour = (200, 200, 255)
            
                cv2.putText(image, text, (2,20), cv2.FONT_HERSHEY_PLAIN, 1.0, textcolour)
    
                if status:
                    self.send_response(200)
                    self.send_header("Content-type", "image/jpg")
                    self.end_headers()
                    st, buffger = cv2.imencode(".jpg", image)
                    self.wfile.write(buffger.tostring())
                    self.wfile.close()
                    ledborg.flashColour(ledborg.GREEN)
                else:
                    #Something went wrong while creating the image,
                    #Send 500 Internal Server Error
                    self.send_error(500, "Image capture failed")
                    ledborg.flashColour(ledborg.MAGENTA)
    
            except IOError:
                self.send_error(404, "File Not Found: %s" % self.path)
                ledborg.flashColour(ledborg.MAGENTA)
                
        else:
            #Unknown URI
            self.send_error(403, "Forbidden")
            log("Headers in forbidden request:")

            for line in self.headers:
                log(line + ": " + self.headers.get(line))
                
            ledborg.flashColour(ledborg.RED)    

def log(msg):
    toLog = '[' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '] ' + msg
    print toLog
    if logging:
        logFile.write(toLog + "\n")
        
try:
    logFile = open(os.path.basename(__file__) + ".log", "a")
    logging = True

except Exception, e:
    print "Logging disabled, %s" %e
        
try:        
    #Open the cat cam
    camera = cv2.VideoCapture(0)

    #For sound playback
    pygame.init()
    
    #Create the web server to serve the cat pics
    server = HTTPServer(('', PORT_NUMBER), PiPurrServer)
    log("Server started on port " + str(PORT_NUMBER))
    
    while(True):
        server.handle_request()

except KeyboardInterrupt:
    log("Shutting down...")
    logFile.close()
    server.socket.close()
    feeder.shutdown()
