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

import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nickjds' 

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/verify_pin", methods=['POST'])
def verify_pin():
	pin_number = request.form['pin_number']
	URL = "http://ffa1a4bd.ngrok.io/api/verify_pin_number/?pin_number=" + pin_number + "&api_endpoint=me.endpnt" 

	r = requests.post(URL)
	response = json.loads(r.text)
	if response['status'] == "SUCCESS":
		conn = sqlite3.connect('reef_monitor.db')
                cur = conn.cursor()
                cur.execute("SELECT token from users where token = ? limit 1", (response['token'],))
                rows = cur.fetchall()
		if any(rows): 
			object = rows[0]
			conn.execute("UPDATE users  SET token = ? WHERE id = ?", (response['token'], object[0]))
			conn.close()
		else:
        		c = conn.cursor()
			c.execute("INSERT INTO users (token) values (?)", (response['token'],))
			conn.commit()
			conn.close()
	return str(response['status'])

@app.route("/api/sync_sensors/all", methods=['POST'])
def sync_sensors():
	try:
		decoded = jwt.decode(request.args.get('token'), 'iliketurtles', algorithms=['HS256'])
		conn = sqlite3.connect('reef_monitor.db')
		cur = conn.cursor()
		cur.execute("SELECT token from users where token = ? limit 1", (decoded['auth_token'],))
		rows = cur.fetchall()
		if any(rows):
			cur.execute("UPDATE users SET sensors  = ? WHERE token = ?", (str(json.dumps(decoded['sensors'])), decoded['auth_token']))
			conn.commit()
			conn.close()
		return str(decoded)
		conn.close()
	except IOError as e:
                return e.to_json

@app.route("/api/device_status/all", methods=['POST'])
def get_status_all():
        try:
		decoded = jwt.decode(request.args.get('token'), 'iliketurtles', algorithms=['HS256'])
		conn = sqlite3.connect('reef_monitor.db')
                cur = conn.cursor()
                cur.execute("SELECT token from users where token = ? limit 1", (decoded['auth_token'],))
                rows = cur.fetchall()
		conn.close()
                if any(rows):
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
        decoded = jwt.decode(request.args.get('token'), 'iliketurtles', algorithms=['HS256'])
        conn = sqlite3.connect('reef_monitor.db')
        cur = conn.cursor()
        cur.execute("SELECT token from users where token = ? limit 1", (decoded['auth_token'],))
        rows = cur.fetchall()
        conn.close()
        if any(rows):
                temp = TempSensor()
                sensor = temp.sensor()
                return jsonify(temp.get_reading())
        else: 
                return "Unauthorized"

@app.route("/api/turn_on_device", methods=["POST"])
def turn_on_device():
	try:
       	 	decoded = jwt.decode(request.args.get('token'), 'iliketurtles', algorithms=['HS256'])
        	conn = sqlite3.connect('reef_monitor.db')
        	cur = conn.cursor()
        	cur.execute("SELECT token from users where token = ? limit 1", (decoded['auth_token'],))
        	rows = cur.fetchall()
        	conn.close()
        	if any(rows):
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
        	decoded = jwt.decode(request.args.get('token'), 'iliketurtles', algorithms=['HS256'])
                conn = sqlite3.connect('reef_monitor.db')
                cur = conn.cursor()
                cur.execute("SELECT token from users where token = ? limit 1", (decoded['auth_token'],))
                rows = cur.fetchall()
                conn.close()
                if any(rows):
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
