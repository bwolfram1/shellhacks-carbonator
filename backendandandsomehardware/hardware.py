# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony Dicola, Justin Cooper

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, Data, RequestError
import datetime
import serial
import json
import os
import random
from twilio.rest import Client
import time
import sys
from pymongo import MongoClient
from pprint import pprint


comport = sys.argv[1]
dataflag  = sys.argv[2]


# print (mongostring)
client = MongoClient("redactedAZUREKey")
# # redactedS=120000&appName=@hacks@
# client = MongoClient(mongostring)
db = client["shellhacks2022"]



def datasender(payload):
    global db
    global dataflag
    
    if dataflag != "1":
        print ("data not uploaded")
        return
    print ("payload ready")
    print (payload)
    # payload ["reading"] = reading
    result=db.readings.insert_one(payload)
    print (result.inserted_id)
    



def motorcontrol(comport, comm):
    ##ser = serial.Serial('/dev/ttyACM0', 115200)

    ser = serial.Serial(comport, 115200)

    print ("connected to: " + ser.portstr)


        
    if comm == "on":
        print ("motor onnnnnn")
        ser.write(b'1')
        time.sleep(3)
        
    if comm == "off":
        ser.write(b'2')
    

    
    ser.close()




# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'redacted'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'redacted'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
# try:
#     temperature = aio.feeds('temperature')
# except RequestError:
#     feed = Feed(name="temperature")
#     temperature = aio.create_feed(feed)

#
# Adding data
#

# aio.send_data(temperature.key, 42)
# # works the same as send now
# aio.append(temperature.key, 42)

# # setup batch data with custom created_at values
# yesterday = (datetime.datetime.today() - datetime.timedelta(1)).isoformat()
# today = datetime.datetime.now().isoformat()
# data_list = [Data(value=50, created_at=today), Data(value=33, created_at=yesterday)]
# # send batch data
# aio.send_batch_data(temperature.key, data_list)

#
# Retrieving data
#


# print ("raw temperature data next")
# data = aio.receive_next(temperature.key)
# print(data)

# print ("raw temperature data")
# data = aio.receive(temperature.key)
# print(data)

# print ("raw temperature data previous")
# data = aio.receive_previous(temperature.key)
# print(data)


# Get list of feeds.
feeds = aio.feeds()

# Print out the feed names:

for f in feeds:
    print('Feed: {0}'.format(f.name))

    dname = f.name
    
    if "_" in dname: continue
    if "pump" in dname: continue
    if "lights" in dname: continue
    
    
    
    
    if dname == "moisture":
        data = aio.data(dname)
        mval = int(data[0].value)
        print ("moisture value is " + str(data[0].value))
        
        if mval < 400:
            print ("motor on")
            
                ##ser = serial.Serial('/dev/ttyACM0', 115200)

            ser = serial.Serial(comport, 115200)

            print ("connected to: " + ser.portstr)
            
            conf = input("confirm motor on?")
                
            print ("motor onnnnnn")
            ser.write(b'1')
            # ser.write(b'1')
            time.sleep(3)
            conf = input("confirm motor off?")
            
            ser.close()
            
            
            
            # motorcontrol(comport, 'on')
            sdata = Data(value=2)
            aio.create_data('pump', sdata)
        else:
            print ("motor off")
            motorcontrol(comport, 'off')
            sdata = Data(value=1)
            aio.create_data('pump', sdata)
    
    data = aio.data(dname)
    print(dname)

    for d in data:
        payload = {}
        if dname == "led" or dname == 'pump' or dname == 'weedslmao': 
            print('Data value: {0}'.format(d.value))
            print('Timestamp value: {0}'.format(d.created_epoch))
            
            payload['readingname'] = dname
            payload['value'] = str(d.value)
            payload['timestamp'] = str(d.created_epoch)
            payload['plantid'] = "1"
            
            datasender(payload)
            
            
            continue
        
        if float(d.lat) == 0.0 and float(d.lon) == 0.0:
            continue
        print('Data value: {0}'.format(d.value))
        
        print('Latitude value: {0}'.format(d.lat))
        print('Longitude value: {0}'.format(d.lon))
        print('Elevation value: {0}'.format(d.ele))
        print('Timestamp value: {0}'.format(d.created_epoch))
        
        print("*****")
        print (d)
        payload['readingname'] = dname
        payload['value'] = str(d.value)
        payload['timestamp'] = str(d.created_epoch)
        payload['plantid'] = "1"
        
        datasender(payload)
    
    
    
    

# data = aio.data('temperature')
# print("temperature")

# for d in data:
#     if float(d.lat) == 0.0 and float(d.lon) == 0.0:
#         continue
#     print('Data value: {0}'.format(d.value))
#     print('Latitude value: {0}'.format(d.lat))
#     print('Longitude value: {0}'.format(d.lon))
#     print('Elevation value: {0}'.format(d.ele))
#     print('Timestamp value: {0}'.format(d.created_epoch))
    
#     print("*****")
#     print (d)


# data = aio.data('humidity')
# print("humidity")

# for d in data:
#     if float(d.lat) == 0.0 and float(d.lon) == 0.0:
#         continue
#     print('Data value: {0}'.format(d.value))
#     print('Timestamp value: {0}'.format(d.created_epoch))
    
#     print("*****")
#     print (d)
    

# data = aio.data('pressure')
# print("pressure")

# for d in data:
#     if float(d.lat) == 0.0 and float(d.lon) == 0.0:
#         continue
#     print('Data value: {0}'.format(d.value))
#     print('Timestamp value: {0}'.format(d.created_epoch))
    
#     print("*****")
#     print (d)

# data = aio.data('688gas')
# print("688gas")

# for d in data:
#     if float(d.lat) == 0.0 and float(d.lon) == 0.0:
#         continue
#     print('Data value: {0}'.format(d.value))
#     print('Timestamp value: {0}'.format(d.created_epoch))
    
#     print("*****")
#     print (d)

# data = aio.data('co2')
# print("co2")

# for d in data:
#     if float(d.lat) == 0.0 and float(d.lon) == 0.0:
#         continue
#     print('Data value: {0}'.format(d.value))
#     print('Timestamp value: {0}'.format(d.created_epoch))
    
#     print("*****")
#     print (d)
    
    
# data = aio.data('moisture')
# print("moisture")

# for d in data:
#     if float(d.lat) == 0.00 and float(d.lon) == 0.0:
#         continue
#     print('Data value: {0}'.format(d.value))
#     print('Timestamp value: {0}'.format(d.created_epoch))
    
#     print("*****")
#     print (d)

# data = aio.data('soilTemp')
# print("soilTemp")

# for d in data:
#     if float(d.lat) == 0.00 and float(d.lon) == 0.0:
#         continue
#     print('Data value: {0}'.format(d.value))
#     print('Timestamp value: {0}'.format(d.created_epoch))
    
#     print("*****")
#     print (d)
