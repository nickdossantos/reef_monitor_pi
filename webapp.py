#Author Nick Dos Santos
from flask import Flask
from flask import request
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask import jsonify
import RPi.GPIO as GPIO
from temperature import TempSensor
import jwt

import model
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nickjds' 

data = model.Data()

admin = Admin(app, name='Reef Admin Page', template_mode='bootstrap3', url='/')
admin.add_view(ModelView(model.User))
admin.add_view(ModelView(model.Device))
admin.add_view(ModelView(model.Sensor))


@app.route("/api/device_status", methods=['POST'])
def get_status():
	try:
        	GPIO.setmode(GPIO.BCM)
		response = []
		for device in data.get_devices():
			print device
			print device.name
      			GPIO.setup(device.pin, GPIO.OUT) # GPIO Assign mode
			device_status = GPIO.input(device.pin)
			if device_status == 1: 
				device_status = True
			else: 
				device_status = False
			device_obj = {'device':device.identifier, 'status':device_status}
			response.append(device_obj)
	except:
		print("there was an error")
	return jsonify(response)

@app.route("/api/get_temperature_reading", methods=['POST'])
def get_termperature_reading():
	user = data.find_user(request.args.get('auth_token'))
	if user:
		temp = TempSensor()
		sensor = temp.sensor()
		post = temp.post_reading(sensor, user.api_endpoint)
		return "it posted"
	else: 
		return "user could not be found"


@app.route("/api/turn_on_device", methods=["POST"])
def turn_on_device_jwt():
	try:
		token = request.args.get('token')
		print token
       	 	decoded = jwt.decode(token, 'iliketurtles', algorithms=['HS256'])
		print decoded
		auth_token = decoded['auth_token']
		identifier = decoded['identifier']
		if token and identifier:
			user = data.find_user(auth_token)
                	device = data.find_device(identifier)
			print user.name
	                GPIO.setmode(GPIO.BCM)
        	
                	GPIO.setwarnings(False)

                	GPIO.setup(device.pin, GPIO.OUT) # GPIO Assign mode

               		 GPIO.output(device.pin, GPIO.HIGH) # on  

               		return get_status()

		else:
			return "Could not find a user or device with information provided"

        except IOError as e:
                return e.to_json
	
@app.route("/api/turn_off_device", methods=["POST"])
def turn_off_device_jwt():
	try:
        	token = request.args.get('token')
        	print token
        	decoded = jwt.decode(token, 'iliketurtles', algorithms=['HS256'])
        	print decoded
        	auth_token = decoded['auth_token']
        	identifier = decoded['identifier']
        	if token and identifier:
                	user = data.find_user(auth_token)
                	device = data.find_device(identifier)
                	print user.name
                	print device.identifier
                	GPIO.setmode(GPIO.BCM)
        
                	GPIO.setwarnings(False)

                	GPIO.setup(device.pin, GPIO.OUT) # GPIO Assign mode

                	GPIO.output(device.pin, GPIO.LOW) # off  

                	return get_status()

        	else:
                	return "Could not find a user or device with information provided"

        	return "I am done"
	except IOError as e:
		return e.to_json
