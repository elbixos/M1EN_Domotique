import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import time     # Import the time module for the sleep function

GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering

ledpin = 8
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

dureeCycle = 2 # En secondes
try:
    while True: # Run forever
        GPIO.output(ledpin, GPIO.HIGH) # Turn on
        time.sleep(dureeCycle * 0.5 )                  # Sleep for 1 second
        GPIO.output(ledpin, GPIO.LOW)  # Turn off
        time.sleep(dureeCycle * 0.5)

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
