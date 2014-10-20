#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple. Registra los clientes SIP.
"""

import SocketServer
import sys


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        client_ip = str(self.client_address[0])
        client_port = str(self.client_address[1])
        print "IP del cliente: " + client_ip,
        print "| Puerto del cliente: " + client_port
        client_dic = {}

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            param_list = line.split(" ")
            param_list[-1] = param_list[-1].split('\r')[0]
            if param_list != [""]:
                method = param_list[0]
                user = param_list[1]
                version = param_list[2]

                if method == 'REGISTER':
                    client_dic[user] = client_ip
                    self.wfile.write(version + " 200 OK\r\n\r\n")
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        port = int(sys.argv[1])
    except IndexError:
        print ("Usage: python server.py server_port")

    serv = SocketServer.UDPServer(("", port), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
