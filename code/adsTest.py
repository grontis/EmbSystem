import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1015(i2c)

#single ended analog input mode
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)

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
	print(IRValue)
	return

while True:
	getTemp()

	#getIR()
