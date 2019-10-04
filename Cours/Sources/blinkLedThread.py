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

freq = 0.5 # en Hz
clignote = True

ledpin = 8
GPIO.setmode(GPIO.BOARD)                        # Use physical pin numbering
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.LOW)

try:

    monThread = threading.Thread(target=clignoter, args=(ledpin,))
    monThread.start()

    while True:
         print("pg principal")
         print ("entrez la frequence souhaitee")
         freq = float(input())

except (KeyboardInterrupt, SystemExit):
    clignote = False
