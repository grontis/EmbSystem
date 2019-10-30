import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import sys, time
import RPi.GPIO as GPIO
from .LEDController import LEDController

#CONFIGURE ADS CONVERTER WITH RASPBERRY PI
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
#single ended analog input mode
tempChannel = AnalogIn(ads, ADS.P0)
IRChannel = AnalogIn(ads, ADS.P1)

def getTemp():
	temp = 0
	for i in range(5):
		temp += (tempChannel.voltage - .5) /.01
	return temp

def getIR():
	IRValue = 0
	for i in range(5):
		IRValue += IRChannel.value
	print(IRValue)
	return

def main():
    led1 = LEDController(11,13,15)
    led1.redOn()

while(True):
    main()
