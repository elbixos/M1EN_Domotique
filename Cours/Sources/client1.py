import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print ('connecting to', server_address)
sock.connect(server_address)

message = '99'
print ('sending ' message)
sock.sendall(message)

print ('closing socket')
sock.close()
