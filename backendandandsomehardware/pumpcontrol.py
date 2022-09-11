import serial
import json
import os
import random
##from twilio.rest import Client
import time
import sys


comport = sys.argv[1]


##ser = serial.Serial('/dev/ttyACM0', 115200)

ser = serial.Serial(comport, 115200)

print ("connected to: " + ser.portstr)

while True:
    # line = ser.readline()
    # print("read a line")
    # line =line.decode("utf-8")
    # line = line.strip()
    # if line.startswith('#'):
    #     line = line[1:]
    # if line.endswith('$'):
    #     line = line[:-1]
        
    # print(line)
    # command = "sudo python basictransaction.py " + line

    # os.system(command)

    # with open('tstatus.json', 'r') as f:
    #     st = json.load(f)

    comm = input("enter command")
    
    if comm == "on":
        ser.write(b'1')
        continue
        
    if comm == "off":
        ser.write(b'2')
        continue
    
    if comm == "exit":
        break
    
    print ("unknown command")

 
ser.close()
