
import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library

GPIO.setmode(GPIO.BOARD)  # Set Pi to use pin number when referencing GPIO pins.

ledpin = 8

GPIO.setup(ledpin, GPIO.OUT)  # Set GPIO pin 12 to output mode.

freq = 100 # en Hz
pwm = GPIO.PWM(ledpin, freq)   # Initialize PWM on pwmPin 100Hz frequency

dc = 0

while True :
    print ("duty cycle",dc)
    pwm.ChangeDutyCycle(dc)
    dc+= 1
    time.sleep(0.1)
