
#!/usr/bin/env python3
#!/home/pi/.local/lib/python3.7/site-packages

# *****************************************************************************
# Copyright (c) 2014, 2019 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
# *****************************************************************************
<<<<<<< HEAD
from time import sleep
from os import listdir
import json
import signal
import datetime
import subprocess


from sys import path,exit
path.insert(0,"/home/pi")
path.insert(0,"/usr/local/lib/python3.7/dist-packages")
path.insert(0,"/usr/local/lib/python3.7/dist-packages/wiotp/sdk/api/registry")

#### Custom Modules ####
from commands import capture_image, publish_data, load_file
from wiotp.sdk.api.registry import devices
import hologram_commands 
from commandProcessor import commandProcessor
import tensor_flow_process
import db2_publish
#### Custom Modules ####


hologram = hologram_commands.network_connect()
from wiotp_login import client
=======
from sys import path,exit
path.append("/home/pi/.local/lib/python3.7/site-packages")
path.append("/home/pi")
from os import listdir
from subprocess import Popen


import json
import signal
import datetime


#### Custom Modules ####
from commands import capture_image, publish_data, load_file
import hologram_commands 
from commandProcessor import commandProcessor
import tensor_flow_process
#### Custom Modules ####


from time import sleep
import gpiozero as gpz

from uuid import getnode as get_mac

hologram = hologram_commands.network_connect()

try:
    from wiotp.sdk.device import DeviceClient #changed from import wiotp.sdk.device
except ImportError:
    # This part is only required to run the sample from within the samples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import wiotp.sdk"
    from inspect import getfile, currentframe

    cmd_subfolder = path.realpath(
        path.abspath(path.join(path.split(getfile(currentframe()))[0], "../../../src"))
    )
    if cmd_subfolder not in path:
        path.insert(0, cmd_subfolder)
    import wiotp.sdk.device

>>>>>>> 63b8a0f7526410bae2df477df37aaadcd2b71b35
def interruptHandler(signal, frame):
#    hologram_commands.network_disconnect()
    client.disconnect()
    exit(0)

#if the iot.py file is called
if __name__ == "__main__":
    signal.signal(signal.SIGINT, interruptHandler)

    with open('/home/pi/device_info.json') as f:
        data = json.load(f)
    f.close()
<<<<<<< HEAD
    try:
=======

    client = None
    try:
        client = DeviceClient(data['wiotp_info']) # create a client using preset values
>>>>>>> 63b8a0f7526410bae2df477df37aaadcd2b71b35
        client.commandCallback = commandProcessor # set commandCallback to commandProcessor  
        client.connect() # Use MQTT connection to IBM Watson IoT Plateform for publishing events
    except Exception as e:         # store error message in 'e'
        print(str(e))         #  printout error message
        exit(1)         # issue occured, program exit
    print("(Press Ctrl+C to disconnect)")

<<<<<<< HEAD
    i=2 # setting i to be the counter referencing most recent picture
    
    while True:
        street = subprocess.run('ls /home/pi/Pictures',shell=True,stdout=subprocess.PIPE, encoding='utf-8') #list image name insde "images" folder
        street = street.stdout.split('\n')
        if i != len(street)-1:
            image_name = street[len(street)-i]
        else:
            exit()
        print("taking Image")
        ####Keeping the time updated####
       	currDate = datetime.datetime.now().strftime("%d_%m_%y")
       	currTime = datetime.datetime.now().strftime("%H_%M_%S")

        ####capture image function, ref:commands.py####
        #capture_image(currDate,currTime) 
        devices.LogEntry # This is meant to used for debug message from wiotp platform. See reference:"https://ibm-watson-iot.github.io/iot-python/application/api/registry/diag/"
        
        #####invoke ML process#####
        water_stress_lv=tensor_flow_process.ml_process(image_name)
        ###########################

        #####Getting wittyPi Temperature#####
        witty_temp = subprocess.run(['sh','get_temp_witty.sh'], stdout = subprocess.PIPE, encoding = 'utf-8')
        witty_temp = witty_temp.stdout.replace('\n','')
        ####################################
        
        ### invoke method "publish_data" to populate data and format data in a dict format ###
        camera_data = publish_data(currDate,currTime,water_stress_lv,witty_temp)

        ### publish data to wiotp ###
        client.publishEvent('status','json',camera_data)

        ### publish data using hologram webhook ###
        hologram_commands.message_publish(hologram, camera_data)

        ### write data into a data file ###
        with open('/home/pi/data.txt', 'a') as outfile:
            json.dump(camera_data, outfile)
            outfile.write('\n')

        ### Update all camera and image setting ###
        with open('/home/pi/device_info.json') as f:
            data = json.load(f)
        f.close()

        ### Test camera and image setting is changed using website ###
        info = load_file('device','image')
        print(info)
        i=i+1

        ###Publish data to DB2###
        db2_publish.db2_data_publish(camera_data)
        ### Have the system publish data on predetermined interval ###
#        sleep(device_info['statusInterval'])
=======
    street = listdir('/home/pi/images/') #list image name insde "images" folder
    i=0 # setting i to be the counter referencing most recent picture
    while True:
        print("taking Image")
       	currDate = datetime.datetime.now().strftime("%d_%m_%y")
       	currTime = datetime.datetime.now().strftime("%H_%M_%S")
        capture_image(currDate,currTime)
        ####
        water_stress_lv=tensor_flow_process.ml_process(street,i)
        ####
        #Get wittyPi Temperature
        #with open('/home/pi/test.txt','w+') as fout:
        #    wittyPi = Popen(["sudo","/home/pi/wittyPi/wittyPi.sh"],stdout=fout)
        #    sleep(15)
        #    os.system("sudo kill %s" %(wittyPi.pid,))
        #    tempLine = linecache.getline("/home/pi/test.txt",8)
        #    wittyPiTemp = float(tempLine[25:30])
        #    fout.close()
        data = publish_data(currDate,currTime,water_stress_lv)
        hologram_commands.message_publish(hologram, data)
        with open('/home/pi/data.txt', 'a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')
        device_info = load_file('device')
        sleep(device_info['statusInterval'])
>>>>>>> 63b8a0f7526410bae2df477df37aaadcd2b71b35
