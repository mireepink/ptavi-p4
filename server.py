#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor
"""

import SocketServer
import sys

puerto = sys.argv[1]

fichero = open('fichero.txt', 'w')

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Registro SIP
    """
    def handle(self):
		ip = str(self.client_address[0])
		puerto = str(self.client_address[1])
		self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
		while 1:
			line = self.rfile.read()
			line1 = line.split(' ')
			if (line1[0] == 'REGISTER'):
				fichero.write(ip + " " + puerto)

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(puerto)), SIPRegisterHandler)
    print "Lanzando servidor..."
    serv.serve_forever()
