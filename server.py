#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple. Registra los clientes SIP.
"""

import SocketServer
import sys
import time

# Variable global para almacenar los usuarios y sus valores
users_dic = {}


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.ip = str(self.client_address[0])
        self.client_port = str(self.client_address[1])
        print "IP del cliente: " + self.ip,
        print "| Puerto del cliente: " + self.client_port

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line_list = line.split()

            if line_list != []:
                if line_list[0] == 'REGISTER':
                    self.address = line_list[1]
                    self.version = line_list[2]
                    self.expires = float(line_list[4])

                    # Registro del usuario
                    if self.expires != 0:
                        actual_time = time.time()
                        users_dic[self.address] = (self.ip, self.expires,
                                                   actual_time)
                        self.register2file()
                        print "Añadido el usuario " + self.address

                    # Borrado del usuario
                    else:
                        del users_dic[self.address]
                        self.register2file()
                        print "Eliminado el usuario " + self.address
                    self.wfile.write(self.version + " 200 OK\r\n\r\n")

                    # Comprobamos caducidad de usuarios registrados
                    self.check_exp_time()

            if not line:
                break

    def register2file(self):
        """
        Método para imprimir los usuarios registrados en un fichero de texto
        """
        reg_file = open('registered.txt', 'w')
        reg_file.write("User\tIP\tExpires\n")

        for user in users_dic:
            ip = str(users_dic[user][0])
            login_time = users_dic[user][2]
            format_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.gmtime(login_time))
            reg_file.write(user + "\t" + ip + "\t" + format_time + "\n")
        reg_file.close()

    def check_exp_time(self):
        """
        Método para comprobar caducidad de usuarios registrados
        """
        address_list = []
        actual_time = time.time()
        for user in users_dic:
            address_list.append(user)
        for address in address_list:
            expires = users_dic[address][1]
            login_time = users_dic[address][2]
            elapsed_time = actual_time - login_time

            # Si ha expirado el tiempo eliminamos al usuario
            if elapsed_time >= expires:
                del users_dic[address]
                self.register2file()
                print "Tiempo expirado para " + address,
                print "--> Usuario eliminado."

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        port = int(sys.argv[1])
    except IndexError:
        print ("Usage: python server.py server_port")

    serv = SocketServer.UDPServer(("", port), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
