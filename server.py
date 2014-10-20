#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


class  SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
      
    def handle(self):
        self.diccionario = {}
        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            entrada = line.split(' ')
            if entrada[0] == 'REGISTER':
                self.diccionario[entrada[2]] = self.client_address[1]
                print entrada[2] + " 200 " + "OK\r\n\r\n"
            if not line:
                break

if __name__ == "__main__":
    Entrada = sys.argv
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(Entrada[1])),  SIPRegisterHandler)
    print "Lanzando servidor UDP"
    serv.serve_forever()
