import time
import socket
import base64
 
src     = '192.168.86.2'      # ip of remote (Indigo Server)
mac     = '00-00-00-00-00-00' 	# mac of remote
remote  = 'Indigo'        			# remote name
dst     = '192.168.86.4'      # ip of tv
app     = 'python'              # iphone..iapp.samsung
tv      = 'UE32ES6800'          # iphone.UE32ES6800.iapp.samsung
 
def push(key):
  new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  new.connect((dst, 55000))
  msg = chr(0x64) + chr(0x00) +\
        chr(len(base64.b64encode(src)))    + chr(0x00) + base64.b64encode(src) +\
        chr(len(base64.b64encode(mac)))    + chr(0x00) + base64.b64encode(mac) +\
        chr(len(base64.b64encode(remote))) + chr(0x00) + base64.b64encode(remote)
  pkt = chr(0x00) +\
        chr(len(app)) + chr(0x00) + app +\
        chr(len(msg)) + chr(0x00) + msg
  new.send(pkt)
  msg = chr(0x00) + chr(0x00) + chr(0x00) +\
        chr(len(base64.b64encode(key))) + chr(0x00) + base64.b64encode(key)
  pkt = chr(0x00) +\
        chr(len(tv))  + chr(0x00) + tv +\
        chr(len(msg)) + chr(0x00) + msg
  new.send(pkt)
  new.close()
  time.sleep(0.1)
  
def tvOff():
  push("KEY_POWEROFF")

def HDMI1():
  push("KEY_EXT20")

def HDMI2():
  push("KEY_AUTO_ARC_PIP_WIDE")

def HDMI3():
  push("KEY_AUTO_ARC_PIP_RIGHT_BOTTOM")

def HDMI4():
  push("KEY_AUTO_ARC_AUTOCOLOR_FAIL")
