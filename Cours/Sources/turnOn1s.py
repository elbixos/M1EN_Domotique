import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import time     # Import the time module for the sleep function

GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

GPIO.output(8, GPIO.HIGH) # Turn on
time.sleep(1)                  # Sleep for 1 second

GPIO.output(8, GPIO.LOW)  # Turn off

GPIO.cleanup()       # clean up GPIO on CTRL+C exit
