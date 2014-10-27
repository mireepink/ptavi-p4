#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor
"""

import SocketServer
import sys
import time


class  SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Clase SIPRegisterHandler
    """
    lista = []
    diccionario = {}
    
    def register2file(self):
        """
        Metodo que rellena el fichero
        """
        fich = open('registered.txt','w')
        fich.write("User" + "\t" + "IP" + "\t" + "Expires" + "\r\n")
        for direccion in self.diccionario.keys():
            fich.write(direccion + '\t' + self.diccionario[direccion][0] + '\t')
            fich.write(time.strftime('%Y-%m-%d %H:%M:%S',\
                time.gmtime(self.diccionario[direccion][1])) + "\r\n")
        fich.close()

    def handle(self):
        """
        Metodo handle
        """
        while 1:
            line = self.rfile.read()
            entrada = line.split(' ')
            if entrada[0] == 'REGISTER':
                hora = float(time.time())+ float(entrada[5])
                self.lista = [self.client_address[0],hora] 
                self.diccionario[entrada[2]] = self.lista
                hora_actual = float(time.time())
                for direccion in self.diccionario.keys():
                    if self.diccionario[direccion][1] < hora_actual:
                        del self.diccionario[direccion]
                if int(entrada[5]) == 0:
                    del self.diccionario[entrada[2]]
                print entrada[3] + " 200 " + "OK\r\n\r\n"
                self.wfile.write(entrada[3] + " 200 " + "OK\r\n\r\n")
            if not line:
                break
            self.register2file()
            print self.diccionario

if __name__ == "__main__":
    """
    Procedimiento principal
    """
    Entrada = sys.argv
    serv = SocketServer.UDPServer(("", int(Entrada[1])),  SIPRegisterHandler)

    print "Lanzando servidor UDP"
    serv.serve_forever()
