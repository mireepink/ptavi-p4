#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        print "IP del cliente: " + str(self.client_address[0]),
        print "| Puerto del cliente: " + str(self.client_address[1])
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente nos manda " + line
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        port = int(sys.argv[1])
    except IndexError:
        print ("Usage: python server.py server_port")

    serv = SocketServer.UDPServer(("", port), EchoHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
