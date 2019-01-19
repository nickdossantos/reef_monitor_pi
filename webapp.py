#Author Nick Dos Santos
from flask import Flask
from flask import request
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask import jsonify
import RPi.GPIO as GPIO
import jwt

import model

# Create a basic flask app.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mosfet'  # You should probably change this to a random value!

data = model.Data()

# Add an admin view for the Peewee ORM-based DHT sensor and sensor reading models.
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

@app.route("/api/turn_off_relay", methods=['POST'])
def turn_off_power():
        GPIO.setmode(GPIO.BCM)
 
        mode = GPIO.getmode()
        print mode


        GPIO.setwarnings(False)

        RELAIS_1_GPIO = 26
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode

        print GPIO.input(26)

        GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # off
        print GPIO.input(26)
        return get_status()

@app.route("/api/turn_on_relay", methods=['POST'])
def turn_on_power():
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
 
        mode = GPIO.getmode()

        GPIO.setwarnings(False)

        RELAIS_1_GPIO = 26
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode

        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on

        return get_status()

@app.route("/api/turn_off_device", methods=["POST"])
def turn_off_device():
	auth_token = request.args.get('auth_token')
	identifier = request.args.get('identifier')	

	user = data.find_user('f6db0eaff9fbedd038a225972eafd746')
	device = data.find_device('kdnxo1d')

	GPIO.setmode(GPIO.BCM)
        
	GPIO.setwarnings(False)

        GPIO.setup(device.pin, GPIO.OUT) # GPIO Assign mode

        GPIO.output(device.pin, GPIO.LOW) # off
	return get_status()


@app.route("/api/turn_on_device", methods=["POST"])
def turn_on_device():
        auth_token = request.args.get('auth_token')
        identifier = request.args.get('identifier')     

        user = data.find_user('f6db0eaff9fbedd038a225972eafd746')
        device = data.find_device('kdnxo1d')

        GPIO.setmode(GPIO.BCM)
        
        GPIO.setwarnings(False)

        GPIO.setup(device.pin, GPIO.OUT) # GPIO Assign mode

        GPIO.output(device.pin, GPIO.HIGH) # on  

        return get_status()
