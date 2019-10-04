import socket
import sys

freq = sys.argv[1]

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (127.0.0.1, 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:

    # Send data
    message = "clignote "+str(freq)
    print ("sending ",message)
    sock.sendall(message)

except Exception as ex:
    print ex
    raw_input()

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
