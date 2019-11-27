from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import argparse
import datetime

import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import sys, time
import RPi.GPIO as GPIO


#######################
#Code for AWS below
#######################

# Shadow JSON schema:
#
# Name: Bot
# {
#	"state": {
#		"desired":{
#			"property":<INT VALUE>
#		}
#	}
# }

# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        print("ShadowUpdate Accepted")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")

args = parser.parse_args()
host = "a37zzqz465wad2-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "/home/pi/EmbSystem/keys/AmazonRootCA1.pem"
certificatePath = "/home/pi/EmbSystem/keys/pi-certificate.pem.crt.txt"
privateKeyPath = "/home/pi/EmbSystem/keys/pi-private.pem.key"
port = args.port
useWebsocket = args.useWebsocket
thingName = "RaspberryPi"
clientId = "RaspberryPi"

if args.useWebsocket and certificatePath and privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not certificatePath or not privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Init AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = None
if useWebsocket:
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId, useWebsocket=True)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

# Delete shadow JSON doc
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

#######################
#End AWS Code
#######################


#########################
#Code for sensors and LEDS below
#########################

GPIO.cleanup()

#CONFIGURE ADS CONVERTER WITH RASPBERRY PI
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
#single ended analog input mode
tempChannel = AnalogIn(ads, ADS.P0)
IRChannel = AnalogIn(ads, ADS.P1)

#temperature threshhold for thermastat
threshold = 81.0

#IR sensor bounds
closeLowerBound = 20000.0
farLowerBound = 10000.0
farUpperBound = 16000.0


#passcode variables
passcodeEntered = False
passcodeSequence = 0
passcode = '10'

#Initialize RGB LEDs to off at start
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, GPIO.LOW)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.LOW)

def main():
    global passcodeEntered
    global passcodeSequence
    global passcode

    led2 = LEDController(23, 24, 25)

    if  passcodeEntered == False:

        #blink Password LED red
        led2.redOn()
        time.sleep(0.005)
        led2.redOff()

        motionInput = ''
        irReading = getIR()

        if irReading > closeLowerBound:
            print("1: Close Motion " + str(irReading))
            motionInput = '1'
            time.sleep(0.05)

        if farLowerBound < irReading < farUpperBound:
            print("0: Far motion " + str(irReading))
            motionInput = '0'
            time.sleep(0.05)

        if motionInput == passcode[passcodeSequence] and motionInput != '' and passcodeEntered == False:
            if len(passcode) - 1 == passcodeSequence:
                passcodeEntered = True
                passcodeSequence = 0
            else:
                passcodeSequence += 1
            led2.greenOn()
            time.sleep(0.2)
            led2.greenOff()
        elif motionInput != passcode[passcodeSequence] and motionInput != '' and passcodeEntered == False:
            print("Mistake in passcode sequence")
            passcodeSequence = 0
            led2.redOn()
            time.sleep(1)
            led2.redOff()

        if passcodeEntered:
            led2.greenOn()
            print("Password entered correctly.")
        time.sleep(0.2)

    if passcodeEntered:
        tempReading = getTemp()

        led1 = LEDController(17, 27, 22)
        if tempReading< threshold - 8:
            led1.allOff()
            led1.magentaOn()
        elif threshold-8 < tempReading < threshold-4:
            led1.allOff()
            led1.blueOn()
        elif threshold-4 < tempReading < threshold-2:
            led1.allOff()
            led1.cyanOn()
        elif threshold-2 < tempReading < threshold + 2:
            led1.allOff()
            led1.greenOn()
        elif threshold+2 < tempReading < threshold+4:
            led1.allOff()
            led1.yellowOn()
        elif threshold+4 < tempReading:
            led1.allOff()
            led1.redOn()

        print(tempReading)
        currentTime = datetime.datetime.now()
        currentTime = currentTime.strftime("%m/%d/%Y, %H:%M:%S")
        payload = {"state": {"reported": {"temp": str(tempReading),"time": currentTime}}}
        deviceShadowHandler.shadowUpdate(json.dumps(payload), customShadowCallback_Update, 5)


        time.sleep(0.5)

def getTemp():
    tempF = 0
    for i in range(20):
        #get celsius reading from sensor
        temp = (tempChannel.voltage - .5) /.01
        #then convert to F
        tempF += temp * (1.8) + 32
    #average 5 readings
    tempF = tempF / 20
    return tempF

def getIR():
	IRValue = 0
	for i in range(5):
		IRValue += IRChannel.value
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

    def allOff(self):
        self.turnOff(self.redPin)
        self.turnOff(self.greenPin)
        self.turnOff(self.bluePin)


while(True):
    main()
