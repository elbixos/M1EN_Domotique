import socket
import sys

freq = sys.argv[1]

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("127.0.0.1", 10000)
print ('connecting to port ', server_address,file=sys.stderr)
sock.connect(server_address)



try:

    # Send data
    message = "clignote "+str(freq)
    print ('sending ', message,file=sys.stderr)
    sock.sendall(message.encode("Utf8"))

except Exception as ex:
    print (ex)

finally:
    print ('closing socket',file=sys.stderr)
    sock.close()
