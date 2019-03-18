#Author Nick Dos Santos
from flask import Flask
from flask import request
from flask import render_template
from flask_admin import Admin
from flask import jsonify
from dotenv import load_dotenv
from temperature import TempSensor
import json
import requests

import RPi.GPIO as GPIO

import jwt
import os
import model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nickjds' 

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/verify_pin", methods=['POST'])
def verify_pin():
	#post pin to web app verifying the user.
	#get response if user is already verified return message, 
	#if user was veryified send sucess.
	#if there was an error print the error.
	pin_number = request.form['pin_number']
	URL = "http://1992cfd8.ngrok.io/api/verify_pin_number/?pin_number=" + pin_number
	# defining a params dict for the parameters to be sent to the API 
	PARAMS = {'pin_number':pin_number} 
  
	# sending get request and saving the response as response object 
	r = requests.post(URL)
	response = json.loads(r.text)
	print response
	print "this is r"
	return str(response['status'])
@app.route("/api/device_status/all", methods=['POST'])
def get_status_all():
        try:
		decoded = jwt.decode(request.args.get('token'), 'iliketurtles', algorithms=['HS256'])
                if decoded['auth_token'] == os.getenv("AUTH_TOKEN"):
                	GPIO.setmode(GPIO.BCM)
                	response = []
                	for device in decoded['devices']:
                        	GPIO.setup(device['pin_number'], GPIO.OUT) # GPIO Assign mode
                        	device_status = GPIO.input(device['pin_number'])
                        	if device_status == 1: 
                                	device_status = True
                        	else: 
                                	device_status = False
                        	device_obj = {'device': device['id'], 'status': device_status}
                        	response.append(device_obj)
		return jsonify(response)
        except IOError as e:
                return e.to_json

def get_status(devices):
        try:
		GPIO.setmode(GPIO.BCM)
        	response = []
                for device in devices:
			GPIO.setup(device['pin_number'], GPIO.OUT) # GPIO Assign mode
                        device_status = GPIO.input(device['pin_number'])
                        if device_status == 1: 
				device_status = True
			else: 
				device_status = False
			device_obj = {'device': device['id'], 'status': device_status}
                        response.append(device_obj)
                return jsonify(response)
        except IOError as e:
                return e.to_json

@app.route("/api/get_temperature_reading", methods=['GET'])
def get_termperature_reading():
        load_dotenv()
        decoded = jwt.decode(request.args.get('token'), 'iliketurtles', algorithms=['HS256'])
	if decoded['auth_token'] == os.getenv("AUTH_TOKEN"):
                temp = TempSensor()
                sensor = temp.sensor()
                return jsonify(temp.get_reading())
        else: 
                return "Unauthorized"

@app.route("/api/turn_on_device", methods=["POST"])
def turn_on_device():
	try:
		load_dotenv()
       	 	decoded = jwt.decode(request.args.get('token'), 'iliketurtles', algorithms=['HS256'])
		if decoded['auth_token'] == os.getenv("AUTH_TOKEN"):
	                GPIO.setmode(GPIO.BCM)
        	
                	GPIO.setwarnings(False)

                	GPIO.setup(decoded['pin_number'], GPIO.OUT) # GPIO Assign mode

               		GPIO.output(decoded['pin_number'], GPIO.HIGH) # on  

               		return get_status(decoded['devices'])

		else:
			return "Could not find a user or device with information provided"

        except IOError as e:
                return e.to_json
	
@app.route("/api/turn_off_device", methods=["POST"])
def turn_off_device():
	try:
		load_dotenv()
        	decoded = jwt.decode(request.args.get('token'), 'iliketurtles', algorithms=['HS256'])
        	if decoded['auth_token'] == os.getenv("AUTH_TOKEN"):
                	GPIO.setmode(GPIO.BCM)
        
                	GPIO.setwarnings(False)

                	GPIO.setup(decoded['pin_number'], GPIO.OUT) # GPIO Assign mode

                	GPIO.output(decoded['pin_number'], GPIO.LOW) # off  

                	return get_status(decoded['devices'])

        	else:
                	return "Could not find a user or device with information provided"

        	return "I am done"
	except IOError as e:
		return e.to_json

if __name__ == "__webapp__":
	app.run()
