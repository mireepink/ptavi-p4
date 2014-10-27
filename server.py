#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import SocketServer
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIPRegisterHandler class
    """
    def handle(self):
        """
        Se encarga de guardarme en un diccionario
        el cliente, su IP y su tiempo Expires al recibir un REGISTER,
        además de ir eliminando los clientes cuando Expires=0
        """
        while 1:
            line = self.rfile.read()
            if not line:
                break
            line_list = line.split(' ')
            IP = self.client_address[0]
            if line_list[0] == 'REGISTER':
                direccion = line_list[1].split(':')[1]
                expires = int(line_list[4])
                timenow = time.time()
                timexp = timenow + expires
                valores = [IP, timexp]
                diccionario[direccion] = valores
                print diccionario
                print "Enviando ", "SIP/2.0 200 OK" + " REGISTER" + '\r\n\r\n'
                self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
                self.register2file()
                for direccion in diccionario.keys():
                    if timenow >= diccionario[direccion][1]:
                        del diccionario[direccion]
                        print direccion + " ha sido borrado" + '\r\n'
                        print diccionario
                self.register2file()

    def register2file(self):
        """
        Su función es la de escribir en el fichero los usuarios
        con su IP y tiempo e ir eliminándolos cuando corresponda
        """
        fich = open('registered.txt', 'w')
        fich.write("User\tIP\tExpires\r\n")
        for Client in diccionario.keys():
            IP = diccionario[Client][0]
            timexp = diccionario[Client][1]
            time_new = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timexp))
            fich.write(Client + '\t' + IP + '\t' + time_new + '\r\n')

if __name__ == "__main__":
    """
    Creamos un servidor y escuchamos
    """
    diccionario = {}
    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..." + '\r\n'
    serv.serve_forever()
