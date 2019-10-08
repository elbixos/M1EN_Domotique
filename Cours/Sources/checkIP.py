import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("10.2.3.115", 10001)
print ('connecting to port ', server_address)
sock.connect(server_address)



try:

    # Send data
    data = sock.recv(256).decode("Utf8")
    print ('received ', data)

except Exception as ex:
    print (ex)

finally:
    print ('closing socket')
    sock.close()
