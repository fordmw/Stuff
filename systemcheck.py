'''
	PROJEKT: Systemkonfiguration Prufung
	ZWECK: um eine Liste der konfigurierten Elemente innerhalb einer Server bereitstellen
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
from socket import AF_INET, AF_INET6, inet_ntop
from ctypes import (
	Structure, Union, POINTER, pointer, get_errno, cast, c_ushort, c_byte,
	c_void_p, c_char_p, c_uint, c_int, c_uint16, c_uint32
)
import ctypes.util
import ctypes

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
	result = re.search('md0', mdstat)
	result = result.group(0)
	if result == "md0":
		print "This system uses software raid"
result = os.path.isfile("/usr/local/tw/tw_cli")
if result:
	twcli = commands.getoutput("/usr/local/tw/tw_cli info c0")
	result = re.search('RAID-1', twcli)
	result = result.group(0)
	if result == "RAID-1":
		print "This system uses hardware RAID-1"
	result = re.search('RAID-5', twcli)
	result = result.group(0)
	if result == "RAID-5":
		print "This system uses hardware RAID-5"
	result = re.search('RAID-6', twcli)
	result = result.group(0)
	if result == "RAID-6":
		print "This system uses hardware RAID-6"
	result = re.search('RAID-10', twcli)
	result = result.group(0)
	if result == "RAID-10":
		print "This system uses hardware RAID-10"

# NICs and IPs
class struct_sockaddr(Structure):
	_fields_ = [('sa_family', c_ushort),('sa_data', c_byte * 14),]

class struct_sockaddr_in(Structure):
	_fields_ = [('sin_family', c_ushort),('sin_port', c_uint16),('sin_addr', c_byte * 4)]

class struct_sockaddr_in6(Structure):
	_fields_ = [('sin6_family', c_ushort),('sin6_port', c_uint16),('sin6_flowinfo', c_uint32),('sin6_addr', c_byte * 16),('sin6_scope_id', c_uint32)]

class union_ifa_ifu(Union):
	_fields_ = [('ifu_broadaddr', POINTER(struct_sockaddr)),('ifu_dstaddr', POINTER(struct_sockaddr)),]

class struct_ifaddrs(Structure):
	pass

struct_ifaddrs._fields_ = [('ifa_next', POINTER(struct_ifaddrs)),('ifa_name', c_char_p),('ifa_flags', c_uint),('ifa_addr', POINTER(struct_sockaddr)),('ifa_netmask', POINTER(struct_sockaddr)),('ifa_ifu', union_ifa_ifu),('ifa_data', c_void_p)]

libc = ctypes.CDLL(ctypes.util.find_library('c'))

def ifap_iter(ifap):
	ifa = ifap.contents
	while True:
		yield ifa
		if not ifa.ifa_next:
			break
		ifa = ifa.ifa_next.contents

def getfamaddr(sa):
	family = sa.sa_family
	addr = None
	if family == AF_INET:
		sa = cast(pointer(sa), POINTER(struct_sockaddr_in)).contents
		addr = inet_ntop(family, sa.sin_addr)
	elif family == AF_INET6:
		sa = cast(pointer(sa), POINTER(struct_sockaddr_in6)).contents
		addr = inet_ntop(family, sa.sin6_addr)
	return family, addr

class NetworkInterface(object):
	def __init__(self, name):
		self.name = name
		self.index = libc.if_nametoindex(name)
		self.addresses = {}
	def __str__(self):
		return "%s [index=%d, IPv4=%s, IPv6=%s]" % (self.name, self.index,self.addresses.get(AF_INET),self.addresses.get(AF_INET6))

def get_network_interfaces():
	ifap = POINTER(struct_ifaddrs)()
	result = libc.getifaddrs(pointer(ifap))
	if result != 0:
		raise OSError(get_errno())
	del result
	try:
		retval = {}
		for ifa in ifap_iter(ifap):
			name = ifa.ifa_name
			i = retval.get(name)
			if not i:
				i = retval[name] = NetworkInterface(name)
				family, addr = getfamaddr(ifa.ifa_addr.contents)
			if addr:
				i.addresses[family] = addr
		return retval.values()
	finally:
		libc.freeifaddrs(ifap)

if __name__ == '__main__':
	for ni in get_network_interfaces():
		print str(ni)
