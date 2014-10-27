#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""
import sys
import SocketServer


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    
    def handle(self):
        print self.client_address 
        while 1:
	    line = self.rfile.read()
            line_list = line.split(' ')
            if line_list[0] == 'REGISTER':
		direccion = line_list[1].split(':')[1]
                diccionario[direccion] =  self.client_address[0]
                print "Enviando", "SIP/2.0 200 OK" + '\r\n\r\n' 
                self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
            if not line:
                break
        

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    diccionario = {}
    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
