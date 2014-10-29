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
users = {}


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """
        Método para recibir en el manejador y gestionar registro de usuarios
        """
        # Escribe dirección y puerto del cliente (de tupla client_address)
        ip = str(self.client_address[0])
        port = str(self.client_address[1])
        print "IP del cliente: " + ip + "| Puerto del cliente: " + port

        while 1:
            # Leyendo carácter a carácter lo que nos envía el cliente
            line = self.rfile.read()
            lines = line.split()

            if lines != []:
                if lines[0] == 'REGISTER':
                    address = lines[1]
                    version = lines[2]
                    expires = float(lines[4])

                    # Comprobamos caducidad de usuarios registrados
                    self.check_expires()

                    # Registro del usuario
                    if expires != 0:
                        users[address] = (ip, expires, time.time())
                        self.register2file()
                        print "Añadido el usuario " + address
                    # Borrado del usuario (si existe en el diccionario)
                    else:
                        found = 0
                        for user in users:
                            if address == user:
                                found = 1
                        if found:
                            del users[user]
                            self.register2file()
                            print "Eliminado el usuario " + user
                        else:
                            print "El usuario no se encuentra en el registro"
                    self.wfile.write(version + " 200 OK\r\n\r\n")

            if not line:
                break

    def register2file(self):
        """
        Método para imprimir los usuarios registrados en un fichero de texto
        """
        users_file = open('registered.txt', 'w')
        users_file.write('User' + '\t' + 'IP' + '\t' + 'Expires' + '\n')

        for user in users:
            ip = str(users[user][0])
            log_time = users[user][2]
            format_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.gmtime(log_time))
            users_file.write(user + "\t" + ip + "\t" + format_time + "\n")
        users_file.close()

    def check_expires(self):
        """
        Método para comprobar caducidad de usuarios registrados
        """
        addresses = []
        for user in users:
            addresses.append(user)
        for address in addresses:
            expires = users[address][1]
            log_time = users[address][2]
            elapsed_time = time.time() - log_time

            # Si ha expirado el tiempo eliminamos al usuario
            if elapsed_time >= expires:
                del users[address]
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
    print "Lanzando servidor SIP..."
    serv.serve_forever()
