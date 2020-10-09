# Embedded Systems Fall 2019 Project: SmartTemp

## Introduction

This project was created with the objective of using temperature sensor readings to automate colored lighting based on temperature. The system was created with consideration to possible use cases in both home and business situations. The thermostat is programmed with a threshold value in the code, and the lighting is output to an RGB LED based on varying comparisons of the temperature reading with the threshold value. An infrared distance sensor is also used for the purpose of entering a sequence of motions as a passcode to the system. The “smart” aspect of the system is achieved by integrating the hardware components and local software with cloud computing services. Amazon Web Services is used as a cloud provider for this project. 

![diagram1](https://github.com/grontis/EmbSystem/blob/master/imgs/diagram1.png)

## Temperature and Lighting
The system uses a temperature sensor (MCP9700) to read temperature by outputting analog temperature values. The code is configured to read temperature values, and then set output values for an RGB LED color gradient based on a threshold value in the code and the temperature value being read. For example, if the temperature reading is much lower than the threshold then the LED output will be cooler colors (purple, blue, cyan), and if the temperature reading is much higher than the threshold, then the LED output will be warmer colors (yellow, red). If the temperature reading is in range of the threshold then the output will be green.

The temperature sensor outputs raw analog values to the Raspberry Pi. These values must be converted to the corresponding Celsius values. The given equation from the temperature sensor datasheet is such that:

![datasheetEquation](https://github.com/grontis/EmbSystem/blob/master/imgs/datasheetEquation.png)

Ta = (Vout – V0c) / Tc 
Ta =  (Vout – .5) / .01
The above equation is used to convert the readings into Celsius within the Python code. This project has chosen to use Fahrenheit as a temperature metric, and so the Celsius values are then converted to Fahrenheit before being used.


## Motion Sensor and Security

An aspect of security was taken into consideration for this project. This was implemented in this project by using an infrared distance sensor (SHARP 2Y0A21) to detect motions. A user’s passcode is represented in the code as a binary string of 0’s and 1’s. The sensor takes readings based on an infrared signal’s reflection to determine distance. The code of the project has been configured such that waving a hand close (approx. 4cm away) through the sensor’s view will be read as an input of 1, and a far motion (approx. 20cm away) will be read as an input of 0.  A blinking RGB LED is used to display correct or incorrect passcode inputs.  This sensor was tested to determine a satisfactory range of what may be considered a “close” motion’s value, and a range of what may be considered a “far” motion’s value. 

![passcodeSequence](https://github.com/grontis/EmbSystem/blob/master/imgs/passcodeSequence.png)

## Cloud IoT with Amazon Web Services (AWS)
Amazon Web Services is used as a cloud services solution. Temperature data is streamed and stored in AWS. This data can be used to create alerts, such as a text message or email alert if the temperature is above a certain value. Further analytics can also be done on the data using AWS services. One feature that was desired from the start of this project was to have a user be updated with an alert via the cloud if a certain temperature threshold is crossed. This is done in AWS by creating a rule to be acted upon when it is needed. Below is an example of a rule used:

![tempRule](https://github.com/grontis/EmbSystem/blob/master/imgs/tempRule.png)

The following diagram shows the flow of IoT data as it is updated to the cloud, and then sent through a data stream through AWS IoT Analytics service. IoT Analytics allows for the data to be queried and retrieved. This data can be exported as a .csv or may even be used in a Jupyter notebook for advance analytics and machine learning purposes. 

![awsDiagram](https://github.com/grontis/EmbSystem/blob/master/imgs/awsDiagram.png)

## Early Designs

Before implementation:

![earlyDesign1](https://github.com/grontis/EmbSystem/blob/master/imgs/earlyDesign1.png)

Design Iteration 10/22/19:

![earlyDesign2](https://github.com/grontis/EmbSystem/blob/master/imgs/earlyDesign2.png)

Design iteration 11/7/19 (everything connected locally, no cloud):

![earlyDesign3](https://github.com/grontis/EmbSystem/blob/master/imgs/earlyDesign3.png)
