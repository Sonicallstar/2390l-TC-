#!/usr/bin/env python !/bin/bash

import RPi.GPIO as GPIO
import bme680
import time
import os
import subprocess
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

print("\n\nPolling:")
"""try:
    while True:
        if sensor.get_sensor_data():
            output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)

            if sensor.data.heat_stable:
                print("{0},{1} Ohms".format(output, sensor.data.gas_resistance))

            else:
                print(output)"""
try:
	while True:

		if sensor.get_sensor_data():
            		output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)

            		if sensor.data.heat_stable:
                		print("{0},{1} Ohms".format(output, sensor.data.gas_resistance))

            		else:
                		print(output)





		current_gas_qual = "The Gas quality sensor reads {0} Ohms".format(sensor.data.gas_resistance)
		current_inside_temp = "The temperature is {0:.2f}C".format(sensor.data.temperature)
		x=x+1	
		#pico2wave -w Current_Inside_Values.wav "$current_inside_temp"
		print (current_inside_temp)
		GPIO.output(7,True)
		time.sleep(1)
		GPIO.output(7,False)
		#os.system('sudo pico2wave -w TEST_1.wav "Is this thing working... I dont think it\'s working"')
		#os.system('aplay TEST_1.wav')
		#os.system('echo $current_inside_temp')
	        #os.system('sudo pico2wave -w TEST_1.wav "The temperature is {0:.2f}C".format(sensor.data.temperature)')
	        #os.system('aplay TEST_1.wav')
		if (x>=30):
			call(["pico2wave","-w","TEST_2.wav",current_gas_qual])
			call(["aplay","TEST_2.wav"])
			call(["pico2wave","-w","TEST_3.wav",current_inside_temp])
                        call(["aplay","TEST_3.wav"])
                        x=0

			x=0
		#file = open("current_temp.txt","w")
		#file.write(current_inside_temp)	
		#file.close()
		
			

except KeyboardInterrupt:
    pass

