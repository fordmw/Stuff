'''
	PROJEKT: Systemkonfiguration Prufung
	ZWECK: um eine Liste der konfigurierten Elemente innerhalb einer Server zu bereitstellen
	DATUM: 29.09.2012
	AUTOR: Bradford Morgan White
'''
import sys
import os
import string
import commands
import fnmatch
import platform
import re
import socket

# Hostnamen apportieren
from socket import gethostname
print "Hostname: " + gethostname()

# 32 oder 64
print platform.platform()

# debian php
try:
	result = os.path.isfile("/usr/bin/php")
except Exception:
	print "Error Parsing Stream"
else:
	if result:
		print "This system has Debian PHP"
	else:
		print "This system does not have Debian PHP"
		
# lokal kompiliertes php
try:
	result = os.path.isfile("/usr/local/bin/php")
except Exception:
	print "Error Parsing Stream"
else:
	if result:
		print "This system has a locally compiled PHP"
	else:
		print "This system does not have a locally compiled PHP"

# welches php aktiviert ist
try:
	result = commands.getoutput('which php')
except Exception:
	print "Could not run shell command"
else:
	if result == "/usr/bin/php":
		print "This system defaults to Debian PHP"
	if result == "/usr/local/bin/php":
		print "This system defaults to a hand compiled PHP"


# Apache 1?
try:
	result = os.path.exists("/etc/apache")
except Exception:
	print "Error Parsing Stream"
else:
	if result:
		for file in os.listdir("/etc/apache/"):
			if fnmatch.fnmatch(file, '*.virt'):
				print "Apache 1 Virt file: " + file
				x = commands.getoutput("ps eax | grep -v grep | grep -c httpd")
				print x + " instances of Apache running"
			else:
				print "There are no Apache1 virt files"

# Apache 2?
try:
	result = os.path.exists("/etc/apache2/sites-enabled/")
except Exception:
	print "Error Parsing Stream"
else:
	if result:
		for file in os.listdir("/etc/apache2/sites-enabled/"):
			if fnmatch.fnmatch(file, '*'):
				print "Apache 2 Virt file: " + file
				x = commands.getoutput("ps eax | grep -v grep | grep -c apach2")
				print x + " instances of Apache2 running"
			else:
				print "There are no Apache2 virt files"

# Nginx?
try:
	result = os.path.exists("/etc/nginx/sites-enabled/")
except Exception:
	print "Error Parsing Stream"
else:
	if result:
		for file in os.listdir("/etc/nginx/sites-enabled/"):
			if fnmatch.fnmatch(file, '*'):
				print "Nginx Virt file: " + file
				x = commands.getoutput("ps eax | grep -v grep | grep -c nginx")
				print x + " instances of nginx running"
			else:
				print "There are no Nginx virt files"

# lighttpd?
try:
	result = os.path.exists("/etc/lighttpd/")
except Exception:
	print "Error Parsing Steam"
else:
	if result:
		print "This system is using Lighttpd"
		print "Check /etc/lighttpd/lighttpd.conf"
		x = commands.getoutput("ps eax | grep -v grep | grep -c lighttpd")
		print x + " instances of lighttpd running"

# Festplatten
result = os.path.isfile("/proc/mdstat")
if result:
	mdstat = commands.getoutput("cat /proc/mdstat")
	m = re.search('md0', mdstat)
	result = m.group(0)
	if result == "md0":
		print "This system uses software raid"
result = os.path.isfile("/usr/local/tw/tw_cli")
if result:
	twcli = commands.getoutput("/usr/local/tw/tw_cli info c0")
	m = re.search('RAID-1', twcli)
	result = m.group(0)
	if result == "RAID-1":
		print "This system uses hardware RAID-1"
	m = re.search('RAID-5', twcli)
	result = m.group(0)
	if result == "RAID-5":
		print "This system uses hardware RAID-5"
	m = re.search('RAID-6', twcli)
	result = m.group(0)
	if result == "RAID-6":
		print "This system uses hardware RAID-6"
	m = re.search('RAID-10', twcli)
	result = m.group(0)
	if result == "RAID-10":
		print "This system uses hardware RAID-10"

# Netzwerkkarte und IP-Addresse
result = os.path.isfile("/proc/net/dev")
if result:
	lines = open("/proc/net/dev", "r").readlines()


def getIpAddresses(self): 
	addrList = socket.getaddrinfo(socket.gethostname(), None) 
	ipList=[] 
	for item in addrList: 
		print "Item:", item 
		ipList.append(item[4][0]) 
	return ipList

for line in lines[]:
	interface, values = line.split(':')
	getIpAddresses(interface);
