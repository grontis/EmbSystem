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

#temperature threshhold for thermastat
threshhold = 80.0

def main():
    led1 = LEDController(17,27,22)
    led2 = LEDController(23,24,25)

    if getTemp()< threshhold:
        led1.blueOn()
    elif getTemp() > threshhold:
        led1.redOn()

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
        self.blink(self.greenPin)

    def blueOn(self):
        self.blink(self.bluePin)

    def yellowOn(self):
        self.blink(self.redPin)
        self.blink(self.greenPin)

    def cyanOn(self):
        blink(self.greenPin)
        blink(self.bluePin)

    def magentaOn(self):
        blink(self.redPin)
        blink(self.bluePin)

    def whiteOn(self):
        blink(self.redPin)
        blink(self.greenPin)
        blink(self.bluePin)

    def redOff(self):
        turnOff(self.redPin)

    def greenOff(self):
        turnOff(self.greenPin)

    def blueOff(self):
        turnOff(self.bluePin)

    def yellowOff(self):
        turnOff(self.redPin)
        turnOff(self.greenPin)

    def cyanOff(self):
        turnOff(self.greenPin)
        turnOff(self.bluePin)

    def magentaOff(self):
        turnOff(self.redPin)
        turnOff(self.bluePin)

    def whiteOff(self):
        turnOff(self.redPin)
        turnOff(self.greenPin)
        turnOff(self.bluePin)

while(True):
    main()
