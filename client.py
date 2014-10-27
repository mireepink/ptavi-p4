#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""
import sys
import socket

# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = sys.argv[1]
PORT = int(sys.argv[2])

# Contenido que vamos a enviar
REGISTER = sys.argv[4]
#EXPIRES = sys.argv[5]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print '\r\n' + "REGISTER sip:" + REGISTER + " SIP/2.0" + '\r\n\r\n'
my_socket.send("REGISTER sip:" + REGISTER + " SIP/2.0")
#print "Expires: " + EXPIRES
#my_socket.send(EXPIRES + '\r\n\r\n')
data = my_socket.recv(1024)

print  data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
