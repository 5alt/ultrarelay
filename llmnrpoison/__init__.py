from SocketServer import TCPServer, UDPServer, ThreadingMixIn
from threading import Thread
from LLMNR import LLMNR
import socket
import settings

settings.init()


class ThreadingUDPLLMNRServer(ThreadingMixIn, UDPServer):
	def server_bind(self):
		MADDR = "224.0.0.252"
		self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		
		self.socket.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MADDR) + socket.inet_aton(settings.Config.IP))
		#self.socket.setsockopt(socket.SOL_SOCKET, 25, IP+'\0')
		
		UDPServer.server_bind(self)

ThreadingUDPLLMNRServer.allow_reuse_address = 1

def serve_LLMNR_poisoner(host, port, handler):
	try:
		server = ThreadingUDPLLMNRServer((host, port), handler)
		server.serve_forever()
	except:
		raise
	print color("[!] ", 1, 1) + "Error starting UDP server on port " + str(port) + ", check permissions or other servers running."


#threads.append(Thread(target=serve_LLMNR_poisoner, args=('', 5355, LLMNR,)))

#serve_LLMNR_poisoner('', 5355, LLMNR)