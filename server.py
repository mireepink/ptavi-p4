#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor SIP
"""

import SocketServer
import sys
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Clase SIPRegisterHandler
    """
    lista = []
    diccionario = {}

    def register2file(self):
        """
        Metodo que rellena el fichero
        """
        fich = open('registered.txt', 'w')
        fich.write("User" + "\t" + "IP" + "\t" + "Expires" + "\r\n")
        for direccion in self.diccionario.keys():
            ip = self.diccionario[direccion][0]
            fich.write(direccion + '\t' + ip + '\t')
            estructura = time.gmtime(self.diccionario[direccion][1])
            fich.write(time.strftime('%Y-%m-%d %H:%M:%S', estructura) + "\r\n")
        fich.close()

    def handle(self):
        """
        Metodo que trata la peticion REGISTER
        """
        while 1:
            line = self.rfile.read()
            if not line:
                break
            entrada = line.split(' ')
            print line
            print entrada
            if entrada[0] == 'REGISTER':
                hora = float(time.time()) + float(entrada[4])
                self.lista = [self.client_address[0], hora]
                self.diccionario[entrada[1]] = self.lista
                hora_actual = float(time.time())
                for direccion in self.diccionario.keys():
                    if self.diccionario[direccion][1] < hora_actual:
                        del self.diccionario[direccion]
                print "Enviando..." + "SIP/2.0 200 OK\r\n\r\n"
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                self.register2file()
            else:
                print "SIP/2.0 400 Badrequest\r\n\r\n"
                self.wfile.write("SIP/2.0 400 bad request\r\n\r\n")

if __name__ == "__main__":
    """
    Procedimiento principal
    """
    Entrada = sys.argv
    serv = SocketServer.UDPServer(("", int(Entrada[1])),  SIPRegisterHandler)

    print "Lanzando servidor SIP"
    serv.serve_forever()
