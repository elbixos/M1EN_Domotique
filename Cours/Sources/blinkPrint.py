# -*- coding: utf-8 -*-
import time
import threading

def clignoter():
  while clignote:
      t = 1/freq
      print ("allume")
      time.sleep(t/2)
      print ("eteint")
      time.sleep(t/2)

  print("j'arrete de clignoter")

freq = 0.5 # en Hz
clignote = True

try:

    monThread = threading.Thread(target=clignoter)
    monThread.start()

    while True:
         print("pg principal")
         print ("entrez la frequence souhaitee")
         freq = float(input())

except (KeyboardInterrupt, SystemExit):
    clignote = False
