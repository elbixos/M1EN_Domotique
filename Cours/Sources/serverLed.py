import socket
import sys

# -*- coding: utf-8 -*-
import time
import threading
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library


def clignoter(broche):

  while clignote:
      t = 1/freq

      GPIO.output(broche, GPIO.HIGH) # Turn on
      time.sleep(t/2)

      GPIO.output(broche, GPIO.LOW)  # Turn off
      time.sleep(t/2)

  print("j'arrete de clignoter")

ledpin = 8
GPIO.setmode(GPIO.BOARD)                        # Use physical pin numbering
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.LOW)
clignote = False

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ("127.0.0.1", 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
print ("waiting")

while True:
  print >>sys.stderr, 'waiting for a connection'
  connection, client_address = sock.accept()

  try:
    print >>sys.stderr, 'connection from', client_address

    data = connection.recv(256)
    print >>sys.stderr, 'received "%s"' % data

    dataSplit = data.split()
    freq = float(dataSplit[1]) # en Hz
    print ("frequence", freq)

    if clignote == False :
        clignote = True

        time.sleep(0.1)
        monThread = threading.Thread(target=clignoter, args=(ledpin,))
        monThread.start()



  except Exception as ex:
    print ex
    clignote = False
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

  finally:

    # Clean up the connection
    connection.close()
