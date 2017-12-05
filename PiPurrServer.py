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

import ledborg
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

if __name__ == "__main__":
    print "Initialising..."
    ledborg.setColour(ledborg.YELLOW)

import cv2
import cv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
from datetime import datetime
import time
import pygame
import feeder
import tv

GPIO.setmode(GPIO.BCM)
PIR_PIN = 14
GPIO.setup(PIR_PIN, GPIO.IN)

PORT_NUMBER = 8081  

logging = False

#Open the cat cam
camera = cv2.VideoCapture(0)

def captureImage(live):
    #Capture the image
    
    ledborg.setColour(ledborg.WHITE)
    camera.release()
    camera.open(0)
            
    #Set image dimensions. v4l and your webcam must support this
    camera.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
            
    status, image = camera.read()
    
    ledborg.setColour(ledborg.OFF)
    
    if (live):            
        text = "PiPurr " + datetime.now().strftime("%H:%M:%S %a %d %b")
    else:
        text = "A woo! " + datetime.now().strftime("%H:%M:%S %a %d %b")
        
    textcolour = (150, 150, 200)
            
    cv2.putText(image, text, (2,20), cv2.FONT_HERSHEY_PLAIN, 1.0, textcolour)
    st, imagebuffer = cv2.imencode(".jpg", image)
    
    return (status, imagebuffer)
        
status, motionimage = captureImage(False) # last captured image on motion detction

#Cat detection with PIR
def catCallback(self):
    log('Cat detected')
    global motionimage
    status, motionimage = captureImage(False)

GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=catCallback)

#HTTP Server class
class PiPurrServer(BaseHTTPRequestHandler):    
    
    def sendCatImage(self, image):
        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()
        
        self.wfile.write(image.tostring())
        self.wfile.close()
        ledborg.flashColour(ledborg.GREEN)
    
    #Override logging function with our own
    def log_message(self, format, *args):
        log(self.address_string() + " (" + str(self.client_address[0]) + ") " + format%args)
        
    #Handler for the GET requests, which is all we are handling...
    def do_GET(self):
        #Ignore favicon requests to keep logs clean
        if "/favicon.ico" in self.path:
            pass
        elif "/tvhdmi1" in self.path:
            tv.HDMI1()
            self.send_response(200, "TV HDMI1 sent OK")

            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write("<!DOCTYPE html>")
            self.wfile.write("<html><head><title>" + os.path.basename(__file__) + "</title></head>")
            self.wfile.write("<body><p>TV turned to HDMI1!</p>")
            self.wfile.write("</body></html>")
            self.wfile.close()
        elif "/tvhdmi2" in self.path:
            tv.HDMI2()
            self.send_response(200, "TV HDMI2 sent OK")

            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write("<!DOCTYPE html>")
            self.wfile.write("<html><head><title>" + os.path.basename(__file__) + "</title></head>")
            self.wfile.write("<body><p>TV turned to HDMI2</p>")
            self.wfile.write("</body></html>")
            self.wfile.close()
        elif "/tvhdmi3" in self.path:
            tv.HDMI3()
            self.send_response(200, "TV HDMI3 sent OK")

            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write("<!DOCTYPE html>")
            self.wfile.write("<html><head><title>" + os.path.basename(__file__) + "</title></head>")
            self.wfile.write("<body><p>TV turned to HDMI3!</p>")
            self.wfile.write("</body></html>")
            self.wfile.close()
        elif "/tvhdmi4" in self.path:
            tv.HDMI4()
            self.send_response(200, "TV HDMI4 sent OK")

            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write("<!DOCTYPE html>")
            self.wfile.write("<html><head><title>" + os.path.basename(__file__) + "</title></head>")
            self.wfile.write("<body><p>TV turned to HDMI4!</p>")
            self.wfile.write("</body></html>")
            self.wfile.close()
        elif "/tvoff" in self.path:
            # Turn TV off
            tv.tvOff()
            self.send_response(200, "TV off sent OK")

            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write("<!DOCTYPE html>")
            self.wfile.write("<html><head><title>" + os.path.basename(__file__) + "</title></head>")
            self.wfile.write("<body><p>TV turned off!</p>")
            self.wfile.write("</body></html>")
            self.wfile.close()

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
            
        elif "/pir.jpeg" in self.path:              
            self.sendCatImage(motionimage)
                    
        elif "/cats.jpeg" in self.path:             
            try:    
                status, liveImage = captureImage(True)
    
                if status:
                    self.sendCatImage(liveImage)
                    
                else:
                    #Something went wrong while creating the image,
                    #Send 500 Internal Server Error
                    self.send_error(500, "Image capture failed")
                    ledborg.flashColour(ledborg.MAGENTA)
    
            except IOError:
                self.send_error(500, "IOError: %s" % self.path)
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
    logFile = open(os.path.basename(__file__) + ".log", "a", 0)
    logging = True

except Exception, e:
    print "Logging disabled, %s" %e
        
try:        

    #For sound playback
    pygame.init()
    
    #Create the web server to serve the cat pics
    server = HTTPServer(('', PORT_NUMBER), PiPurrServer)
    log("Server started on port " + str(PORT_NUMBER))
    
    ledborg.setColour(ledborg.OFF)

    while(True):
        server.handle_request()

except KeyboardInterrupt:
    log("Shutting down...")
    logFile.close()
    server.socket.close()
    feeder.shutdown()
    ledborg.setColour(ledborg.OFF)
    GPIO.cleanup()
