import paho.mqtt.client as mqtt #import the client1
import time
from random import randrange, uniform


from Adafruit_IO import Client, Feed, Data, RequestError
import datetime

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'REDACTED'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'REDACTED'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


############


def on_message(client, userdata, message):
    
    global aio
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    
    obj = str(message.payload.decode("utf-8"))
    if obj == 'Weed':
        data = Data(value=2)
    if obj == 'Crop':
        data = Data(value=1)
    
    aio.create_data('weedslmao', data)               
    
    
    
########################################


## publisher test code

# mqttBroker ="mqtt.eclipseprojects.io" 

# client = mqtt.Client("Temperature_Inside")
# client.connect(mqttBroker) 

# while True:
#     randNumber = uniform(20.0, 21.0)
#     client.publish("TEMPERATURE", randNumber)
#     print("Just published " + str(randNumber) + " to topic TEMPERATURE")
#     time.sleep(1)
    
    

mqttBroker ="test.mosquitto.org"

client = mqtt.Client("BrokerServer")
client.connect(mqttBroker) 

client.loop_start()

client.subscribe("openmv/cropsorweed")
client.on_message=on_message 

time.sleep(30)
client.loop_stop()
