#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
Entrada = sys.argv
IP = Entrada[1]
PORT = int(Entrada[2])
PETICION = Entrada[3]

# Contenido que vamos a enviar
DIRECCION = Entrada[4]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

print "Enviando: " + PETICION + " sip: " + DIRECCION
my_socket.send(PETICION + " sip: " + DIRECCION + ' SIP/1.0 ' + '\r\n\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
