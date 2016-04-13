PiPurr Server
=============

PiPurr is a Remote Cat Interaction System that uses the Raspberry Pi.
It allows you to view and interact with your cats from anywhere.

Requires a recent version of OpenCV for webcam capture.
Flashes colours on a connected LedBorg, an awesome LED add-on, available from www.piborg.com.
Can feed cats via a stepper motor connected to a cat feeder.
Wire a PIR to pin 14 on the Raspberry Pi for cat detection.
Interact with it with the Android client in another repo (PiPurr for Android).

Or connect to it directly and request the following endpoints:

* /cats.jpeg - View webcam images on demand (stills only).
* /pir.jpeg - View the last image captured by triggering the PIR sensor.
* /sound - Play sound.ogg through the Pi's speakers.
* /feed - Rotate a stepper motor 360 degrees. Attahced to a cat feeder this dispenses treats.
 
LedBorg colours:
[GREEN] - Successful GET request serviced.
[BLUE] - Initialising / Successful feed or sound play requested.
[RED] - Forbidden URL requested / Error.

Coming soon (eventually!):
* /live - Video streaming

The meow sound is by Dcrosby at en.wikipedia - http://commons.wikimedia.org/wiki/File:Meow.ogg
Licensed [CC-BY-SA-3.0 ( http://creativecommons.org/licenses/by-sa/3.0/ )].

Tris Linnell
http://canthack.org
