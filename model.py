from peewee import *

db = SqliteDatabase('reef.db', check_same_thread=False)

class Device(Model):
    name = TextField()
    identifier = TextField()
    pin = IntegerField()

    class Meta:
        database = db

class Sensor(Model):
    name = TextField()
    identifier = TextField()
    pin = IntegerField()

    class Meta:
        database = db

class User(Model):
    name = TextField()
    auth_token = TextField()
    api_endpoint = TextField()

    class Meta:
        database = db

class Data(object):
    """Main data access layer class which provides functions to query DHT sensor
    and sensor reading data from the database.
    """

    def __init__(self):
        """Initialize access to the DHT sensor reading database."""
        # Connect to the database.
        db.connect()
        # Make sure the tables are created (safe=True, otherwise they might be
        # deleted!).
        db.create_tables([Device, Sensor, User], safe=True)

    def define_device(self, name, identifier, pin):
        """Define the specified sensor and add it to the database.  If a sensor
        of the same name, type, and pin exists then nothing will be added.
        """
        # Use the get_or_create function in Peewee to automatically try to find
        # a sensor the specified name, type, pin and create it if not found.
        # Very handy!
        Device.get_or_create(name=name, identifier=identifier, pin=pin)

    def get_devices(self):
        """Return a list of all the DHT sensors defined in the database.
        Each instace in the list is a DHTSensor object.
        """
        # Use the select function to get all the sensors (effectively a SQL
        # SELECT * FROM... query).
        return Device.select()


    def define_sensor(self, name, identifier, pin):
        """Define the specified sensor and add it to the database.  If a sensor
        of the same name, type, and pin exists then nothing will be added.
        """
        # Use the get_or_create function in Peewee to automatically try to find
        # a sensor the specified name, type, pin and create it if not found.
        # Very handy!
        Sensor.get_or_create(name=name, identifier=identifier, pin=pin)

    def get_sensors(self):
        """Return a list of all the DHT sensors defined in the database.
        Each instace in the list is a DHTSensor object.
        """
        # Use the select function to get all the sensors (effectively a SQL
        # SELECT * FROM... query).
        return Sensor.select()


    def define_user(self, name, auth_token, api_endpoint):
        """Define the specified sensor and add it to the database.  If a sensor
        of the same name, type, and pin exists then nothing will be added.
        """
        # Use the get_or_create function in Peewee to automatically try to find
        # a sensor the specified name, type, pin and create it if not found.
        # Very handy!
        User.get_or_create(name=name, auth_token=auth_token, api_endpoint=api_endpoint)

    def get_users(self):
        """Return a list of all the DHT sensors defined in the database.
        Each instace in the list is a DHTSensor object.
        """
        # Use the select function to get all the sensors (effectively a SQL
        # SELECT * FROM... query).
        return User.select()

    def find_user(self, auth_token): 
	return User.get(auth_token=auth_token)

    def find_device(self, identifier): 
        return Device.get(identifier=identifier)

    def close(self):
        """Close the connection to the database."""
        db.close()

