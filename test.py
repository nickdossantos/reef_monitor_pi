from temperature import TempSensor

#create and instance of temp sensor

temp = TempSensor()

sensor = temp.sensor()

post = temp.post_reading(sensor)
