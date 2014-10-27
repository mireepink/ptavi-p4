#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

entrada = sys.argv

if len(entrada) != 6:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

IP = entrada[1]
PORT = int(entrada[2])
PETICION = entrada[3].upper()

DIRECCION = entrada[4]
TIEMPO = entrada[5]

LINEA = PETICION + " sip:" + DIRECCION + ' SIP/2.0 ' + '\r\n'
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

print PETICION + " sip:" + DIRECCION
print "Expires: " + TIEMPO
my_socket.send(LINEA + "Expires: " + TIEMPO + '\r\n\r\n')
data = my_socket.recv(1024)
print 'Recibido -- ', data
print "Terminando socket..."

my_socket.close()
print "Fin."
