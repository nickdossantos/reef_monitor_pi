Raspberry Pi Web Application API with Flask. 

WebApp.py is the main application for ReefMonitor Pi. In that file you can see specific routes that preform specific jobs, ex reading and writing user information/device information. In WebApp.py you can also see background scheduler tasks. The background tasks will run once the applciation starts. 

Temperature.py is there all the logic for the temperature sensor lives. That file is accessed by WebApp.py to get recent readings from the sensor.
