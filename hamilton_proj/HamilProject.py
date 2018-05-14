#!/usr/bin/env python

import RPi.GPIO as GPIO
import bme680
import time
import os
import httplib, urllib
from subprocess import call
key = '11FTCW0IQAECSGWH'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT)

sensor = bme680.BME680()
x=0

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

def sensor_upload():
		while True:
    		#upload the temperature, humidity, air quality suggestion, and pressure to thingspeak
                	Temperature =(sensor.data.temperature * 1.8)+32+(-1)
                        Humidity=sensor.data.humidity
                        AirQuality=sensor.data.gas_resistance
                        AirPressure=sensor.data.pressure
			params_a =urllib.urlencode({'field1':Temperature,'field2': Humidity,'field3':AirPressure,'field4': AirQuality, 'key':key})
			#params_t = urllib.urlencode({'field1': Temperature, 'key':key })
			#params_h = urllib.urlencode({'field2': Humidity,'key':key})
			#params_p = urllib.urlencode({'field3': AirPressure,'key':key})
			#params_q = urllib.urlencode({'field4': AirQuality,'key':key})

                        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
                        conn = httplib.HTTPConnection("api.thingspeak.com:80")
                        try:
                        	conn.request("POST", "/update", params_a, headers)
			        response = conn.getresponse()
				time.sleep(1)
		 		"""conn.request("POST", "/update", params_p, headers)
			    	response = conn.getresponse()
				time.sleep(15)
			    	conn.request("POST", "/update", params_h, headers)
			    	response = conn.getresponse()
				time.sleep(15)
		       	    	conn.request("POST", "/update", params_t, headers)
                            	response = conn.getresponse()
				time.sleep(15)"""


                            	print Temperature
			    	print Humidity
			    	print AirQuality
 			    	print AirPressure
                            	print response.status, response.reason
                            	data = response.read()
                            	conn.close()
                        except:
                        	print "connection failed"
                        break


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
			GPIO.output(13,True)
			#call(["pico2wave","-w","Air_Quality.wav",current_gas_qual])
			#call(["aplay","Air_Quality.wav"])
			#call(["pico2wave","-w","Surrounding_Temp.wav",current_inside_temp])           	
			#call(["aplay","Surrounding_Temp.wav"])
            		x=0
			GPIO.output(13,False)
			sensor_upload()
			GPIO.output(13,True)
			time.sleep(1)
			GPIO.output(13,False)

except KeyboardInterrupt:
    pass

