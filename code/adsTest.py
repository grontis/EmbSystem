import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
#single ended analog input mode
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)

passcodeEntered = False
passcodeSequence = 0
passcode = '101'

def getTemp():
	temp = 0
	for i in range(5):
		temp += (chan1.voltage - .5) /.01
	print(temp/5)
	return

def getIR():
	IRValue = 0
	for i in range(5):
		IRValue += chan2.value
	return IRValue/5

while True:
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
		if len(passcode)-1 == passcodeSequence:
			passcodeEntered = True
			passcodeSequence = 0
		else:
			passcodeSequence += 1

	if passcodeEntered:
		print("Password entered correctly.")

	time.sleep(0.2)
