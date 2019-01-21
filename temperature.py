import os
import time,datetime
import requests 
import jwt

class TempSensor(object):
	"""RASPBERRY PI IOT"""
	dateString = '%Y/%m/%d'

	def __init__(self):
		hello = "hello"

	def post_reading(self, ds18b20, api_endpoint):
        	temp = self.read(ds18b20)[1]
        	print "Current temperature : %0.3f F" % temp
        	data = {'value':temp,
        	'sensor':'UhchNqkwJ9w8',
        	'user': 'pxHdcwIYrh6B',
        	'date': datetime.datetime.now().strftime(self.dateString)
       	 	}
        	encoded_jwt = jwt.encode(data, 'iliketurtles', algorithm='HS256')
       	 	print encoded_jwt
        	r = requests.post(url = self.API_ENDPOINT + encoded_jwt)
        	print data

	def sensor(self):
    		for i in os.listdir('/sys/bus/w1/devices'):
        		if i != 'w1_bus_master1':
            			ds18b20 = i
    				return ds18b20

	def read(self, ds18b20):
    		location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    		tfile = open(location)
    		text = tfile.read()
    		tfile.close()
    		secondline = text.split("\n")[1]
    		temperaturedata = secondline.split(" ")[9]
    		temperature = float(temperaturedata[2:])
    		celsius = temperature / 1000
    		farenheit = (celsius * 1.8) + 32
    		return celsius, farenheit

	def loop(self, ds18b20):
    		while True:
        		if read(ds18b20) != None:
            			print "Current temperature : %0.3f C" % read(ds18b20)[0]
            			print "Current temperature : %0.3f F" % read(ds18b20)[1]

	def countdown(self, n, ds18b20):
    		start_time = n
    		started = False 
    		while n >= 0: 
        		if n <= 0:
           			self.countdown(10,ds18b20)
        		elif n == start_time and started == False: 
           			self.post_reading(ds18b20)
           			started = True 
        		if n > 0:
           			time.sleep(1)
           			n = n -1
        	   		print n
	           		print started

	def kill(self):
    		quit()

	def start(self): 
	        serialNum = self.sensor()
        	self.countdown(10,serialNum)
