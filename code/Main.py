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
threshhold = 86.0

#passcode variables
passcodeEntered = False
passcodeSequence = 0
passcode = '101'


def main():
    global passcodeEntered
    global passcodeSequence
    global passcode

    if  passcodeEntered == False:
        motionInput = ''
        if getIR() < 5000.0:
            print("No motion " + str(getIR()))
            motionInput = ''

        if getIR() > 15000.0:
            print("1: Close Motion " + str(getIR()))
            motionInput = '1'

        if 10000.0 < getIR() < 14000.0:
            print("0: Far motion " + str(getIR()))
            motionInput = '0'

        if motionInput == passcode[passcodeSequence] and motionInput != '' and passcodeEntered == False:
            if len(passcode) - 1 == passcodeSequence:
                passcodeEntered = True
                passcodeSequence = 0
            else:
                passcodeSequence += 1
        elif motionInput != passcode[passcodeSequence] and motionInput != '' and passcodeEntered == False:
            print("Mistake in passcode sequence")

        if passcodeEntered:
            print("Password entered correctly.")

    if passcodeEntered:
        led1 = LEDController(17,27,22)
        led2 = LEDController(23,24,25)

        if getTemp()< threshhold:
            led1.redOff()
            led1.blueOn()
        elif getTemp() > threshhold:
            led1.blueOff()
            led1.redOn()

        print(getTemp())

    time.sleep(0.2)

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
		IRValue += chan2.value
	return IRValue/5

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
        self.blink(self.greenPin)
        self.blink(self.bluePin)

    def magentaOn(self):
        self.blink(self.redPin)
        self.blink(self.bluePin)

    def whiteOn(self):
        self.blink(self.redPin)
        self.blink(self.greenPin)
        self.blink(self.bluePin)

    def redOff(self):
        self.turnOff(self.redPin)

    def greenOff(self):
        self.turnOff(self.greenPin)

    def blueOff(self):
        self.turnOff(self.bluePin)

    def yellowOff(self):
        self.turnOff(self.redPin)
        self.turnOff(self.greenPin)

    def cyanOff(self):
        self.turnOff(self.greenPin)
        self.turnOff(self.bluePin)

    def magentaOff(self):
        self.turnOff(self.redPin)
        self.turnOff(self.bluePin)

    def whiteOff(self):
        self.turnOff(self.redPin)
        self.turnOff(self.greenPin)
        self.turnOff(self.bluePin)

while(True):
    main()
