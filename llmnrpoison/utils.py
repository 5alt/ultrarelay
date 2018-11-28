#!/usr/bin/env python
# This file is part of Responder, a network take-over set of tools 
# created and maintained by Laurent Gaffie.
# email: laurent.gaffie@gmail.com
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import re
import logging
import socket
import time
import datetime
import settings

def color(txt, code = 1, modifier = 0):
	return "\033[%d;3%dm%s\033[0m" % (modifier, code, txt)

def RespondWithIPAton():
	return socket.inet_aton(settings.Config.IP)

def Parse_IPV6_Addr(data):
	if data[len(data)-4:len(data)][1] =="\x1c":
		return False
	elif data[len(data)-4:len(data)] == "\x00\x01\x00\x01":
		return True
	elif data[len(data)-4:len(data)] == "\x00\xff\x00\x01":
		return True
	return False