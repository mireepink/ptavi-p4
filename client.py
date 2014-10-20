#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor y envía mensajes SIP
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    METHOD = sys.argv[3].upper()
    SIP_ADDRESS = sys.argv[4]
    EXPIRES = sys.argv[5]
except IndexError:
    print ("Usage: client.py ip puerto register sip_address expires_value")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

request = METHOD + " " + "sip:" + SIP_ADDRESS + " SIP/1.0\r\n" + "Expires: " + EXPIRES + '\r\n\r\n'

print "Enviando:\n" + request
my_socket.send(request)
data = my_socket.recv(1024)
print data

print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
