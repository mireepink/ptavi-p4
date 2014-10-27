#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

Entrada = sys.argv

if len(Entrada) != 6:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

IP = Entrada[1]
PORT = int(Entrada[2])
PETICION = Entrada[3].upper()

DIRECCION = Entrada[4]
TIEMPO = Entrada[5]

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

print PETICION + " sip:" + DIRECCION
print "Expires: " + TIEMPO
my_socket.send(PETICION + " sip: " + DIRECCION + ' SIP/2.0 ' + '\r\n' + "Expires: " + TIEMPO + '\r\n\r\n')
data = my_socket.recv(1024)    
print 'Recibido -- ', data
print "Terminando socket..."

my_socket.close()
print "Fin."
