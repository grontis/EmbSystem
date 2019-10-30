import sys, time
import RPi.GPIO as GPIO

class LEDController:
    def __init__(self, redpin, greenpin, bluepin):
        self.redPin = redpin
        self.greenPin = greenpin
        self.bluePin = bluepin

    def blink(self, pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    def turnOff(self, pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    def redOn(self):
        self.blink(redPin)

    def greenOn(self):
        self.blink(greenPin)

    def blueOn(self):
        self.blink(bluePin)

    def yellowOn(self):
        self.blink(redPin)
        self.blink(greenPin)

    def cyanOn(self):
        blink(greenPin)
        blink(bluePin)

    def magentaOn(self):
        blink(redPin)
        blink(bluePin)

    def whiteOn(self):
        blink(redPin)
        blink(greenPin)
        blink(bluePin)

    def redOff(self):
        turnOff(redPin)

    def greenOff(self):
        turnOff(greenPin)

    def blueOff(self):
        turnOff(bluePin)

    def yellowOff(self):
        turnOff(redPin)
        turnOff(greenPin)

    def cyanOff(self):
        turnOff(greenPin)
        turnOff(bluePin)

    def magentaOff(self):
        turnOff(redPin)
        turnOff(bluePin)

    def whiteOff(self):
        turnOff(redPin)
        turnOff(greenPin)
        turnOff(bluePin)
