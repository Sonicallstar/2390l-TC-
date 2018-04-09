#!/usr/bin/env python

import RPi.GPIO as GPIO
import bme680
import time
import os
from subprocess import call

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)

sensor = bme680.BME680()
x=0

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print("\n\nGenerating Data:")

try:
	while True:
		time.sleep(1)
		if sensor.get_sensor_data():
			output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)

			if sensor.data.heat_stable:
				print("{0},{1} Ohms".format(output, sensor.data.gas_resistance))

			else:
				print(output)


		if (sensor.data.gas_resistance >= 110000):
			current_gas_qual = "The air quality is Excellent, sensor reads {0} Kilo Ohms".format(sensor.data.gas_resistance / 1000)
		if (sensor.data.gas_resistance >= 90000 and sensor.data.gas_resistance < 110000):
			current_gas_qual = "The air quality is Great, sensor reads {0} Kilo Ohms".format(sensor.data.gas_resistance / 1000)
		if (sensor.data.gas_resistance >= 70000 and sensor.data.gas_resistance < 90000):
			current_gas_qual = "The air quality is OK, sensor reads {0} Kilo Ohms".format(sensor.data.gas_resistance / 1000)
		if (sensor.data.gas_resistance >= 50000 and sensor.data.gas_resistance < 70000):
			current_gas_qual = "The air quality is Poor, sensitive persons may suffer, sensor reads {0} Kilo Ohms".format(sensor.data.gas_resistance / 1000)
		if (sensor.data.gas_resistance >= 30000 and sensor.data.gas_resistance < 50000):
			current_gas_qual = "The air quality is Really bad, protection is advised or moving to fresh air. Sensor Reads reads {0} Kilo Ohms".format(sensor.data.gas_resistance / 1000)
		if (sensor.data.gas_resistance < 30000):
			current_gas_qual = "Dangerous air quality, wear heavy protection or move to outdoors. Sensor Reads reads {0} Kilo Ohms".format(sensor.data.gas_resistance / 1000)

		current_inside_temp = "The surrounding temperature is {0:.2f}Degrees Fahrenheit".format((sensor.data.temperature * 1.8)+32+(-1))
		x=x+1	
		print (current_inside_temp)
			
		
		if (x>=32):
			GPIO.output(7,True)
			call(["pico2wave","-w","Air_Quality.wav",current_gas_qual])
			call(["aplay","Air_Quality.wav"])
			call(["pico2wave","-w","Surrounding_Temp.wav",current_inside_temp])
           		call(["aplay","Surrounding_Temp.wav"])
            		x=0
			GPIO.output(7,False)

except KeyboardInterrupt:
    pass

