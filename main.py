from flask import * 
app = Flask (__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/get_temp_sensor")
def post_reef_monitor():
	from temperature import TempSensor
	temp = TempSensor()
	sensor = temp.sensor()
	post = temp.post_reading(sensor)
	return "it posted"

@app.route("/api/turn_off_relay", methods=['POST'])
def turn_off_power():
	import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
 
        mode = GPIO.getmode()
        print mode


        GPIO.setwarnings(False)

        RELAIS_1_GPIO = 26
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode

        print GPIO.input(26)

	GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # off
	print GPIO.input(26)
	return "it is off"

@app.route("/api/turn_on_relay", methods=['POST'])
def turn_on_power():
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
 
	mode = GPIO.getmode()
	print mode


	GPIO.setwarnings(False)

	RELAIS_1_GPIO = 26
	GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode

	print GPIO.input(26)

	GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on

	print GPIO.input(26)
	return "it is on"

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True) 
