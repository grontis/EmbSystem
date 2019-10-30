import sys, time
import RPi.GPIO as GPIO

redPin   = 11
greenPin = 13
bluePin  = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.output(redPin, GPIO.HIGH)
