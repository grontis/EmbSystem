import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import sys, time
import RPi.GPIO as GPIO

#CONFIGURE ADS CONVERTER WITH RASPBERRY PI
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
#single ended analog input mode
tempChannel = AnalogIn(ads, ADS.P0)
IRChannel = AnalogIn(ads, ADS.P1)

def main():
    led1 = LEDController(17,27,22)
    led2 = LEDController(10,9,11)
    led1.redOn()
    led2.redOn()
    print(getTemp())

def getTemp():
    temp = 0
    for i in range(5):
        temp += (tempChannel.voltage - .5) /.01
    temp = temp / 5
    tempF = temp * (1.8) + 32
    return tempF

def getIR():
	IRValue = 0
	for i in range(5):
		IRValue += IRChannel.value
	print(IRValue)
	return

class LEDController:
    def __init__(self, redpin, greenpin, bluepin):
        self.redPin = redpin
        self.greenPin = greenpin
        self.bluePin = bluepin

    def blink(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    def turnOff(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    def redOn(self):
        self.blink(self.redPin)

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

while(True):
    main()
