import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('127.0.0.1', 10000)
print ('starting up on',server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
print ("waiting")

print ('waiting for a connection')
connection, client_address = sock.accept()

print ('connection from', client_address)

data = connection.recv(256)
print ('received ',data)

connection.close()
