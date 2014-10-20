#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple. Registra los clientes SIP.
"""

import SocketServer
import sys

client_dic = {}


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

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            param_list = line.split()

            # Registro SIP del cliente
            if param_list != []:
                if param_list[0] == 'REGISTER':
                    sip_address = param_list[1]
                    version = param_list[2]
                    expires = float(param_list[4])
                    client_dic[sip_address] = client_ip

                    # Si ha pasado el tiempo de expiración borramos el cliente
                    if expires == 0:
                        del client_dic[sip_address]
                        print "Eliminado el cliente " + sip_address
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
