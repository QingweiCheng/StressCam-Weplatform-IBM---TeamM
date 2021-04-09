#!/usr/bin/python3
import sys
sys.path.append("/home/pi/.local/lib/python3.7/site-packages")
sys.path.append("/home/pi")

from picamera import PiCamera
from time import sleep

import datetime
import gpiozero as gpz

import subprocess

from skimage.io import imread #read images
from skimage.transform import resize
from tensorflow import lite as tflite
import numpy as np

import psutil

disk = psutil.disk_usage('/')
disk_percent_used = disk.percent
disk_free = disk.free / 2**30

from Hologram.HologramCloud import HologramCloud

subprocess.call("sudo hologram modem connect",shell=True)
credentials = {'devicekey':'MRVw4T*S'} #'6r)^]p]Q'} #Hologram device key from hologram.io
hologram = HologramCloud(credentials, network='cellular',authentication_type='csrpsk') #Connect to Hologram CLoud, change network to cellular to connect to LTE

sum_RSSI = 0.0
sum_quality = 0.0
num_samples = 5

camera = PiCamera()

curr = datetime.datetime.now()
currDate = curr.strftime("%d_%m_%Y")
currTime = curr.strftime("%H_%M_%S")
camera.resolution=(2592,1944)
#camera.rotation = 180
camera.capture('/home/pi/images/' + curr.strftime("%d_%m_%Y_%H_%M_%S") + '.jpg')

#for i in range(num_samples):
#    signal_strength = hologram.network.signal_strength
#    print('Signal strength: ' + signal_strength)
#    rssi, qual = signal_strength.split(',')
#    sum_RSSI = sum_RSSI +int(rssi)
#    sum_quality = sum_quality +int(qual)
#    time.sleep(2)
#print('Average RSSI' + str(sum_RSSI/num_samples))
#print('Average quality' + str(sum_quality/num_samples))

cpu = gpz.CPUTemperature()
cpu_temp = cpu.temperature
print("CPU Temperature:", cpu_temp)
file = '/home/pi/imagesTest/002433.jpg'
im = imread(file)
print("resizing image")
im_final = resize(im,(200,200))#Model was trained on 200x200 images
# Load TFLite model and allocate tensors.
print("allocating tensors")
interpreter = tflite.Interpreter(model_path="/home/pi/converted_model.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
Xtest = np.array(im_final, dtype = np.float32)

#test model
input_data = np.expand_dims(Xtest,axis=0)
interpreter.set_tensor(input_details[0]['index'], input_data)
print("invoke interpreter")
interpreter.invoke()
# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])
results = np.squeeze(output_data)
print(results)
waterStressLevel = int(np.argmax(results))
percentConfident = results[waterStressLevel]*100

print("Time:", curr.strftime("%d_%m_%Y_%H_%M_%S"))
print("CPUTemp", cpu_temp)
print("Saving image...")
data = {
            "DEVICE_ID": 1,
            "DEVICE_STATUS": "On",
            "WATER_STRESS_LEVEL":waterStressLevel,
            "CPU_TEMPERATURE": cpu_temp,
            "DATE_1":currDate,
            "TIME_1":currTime,
            "SD":disk_percent_used,
            "SD_free":disk_free,
#            "Av_RSSI":sum_RSSI/num_samples,
#            "Av_qual":sum_quality/num_samples,
        }
recv = hologram.sendMessage(data) # Send message to hologram cloud
print("Recieved Code:",recv)
print("0 Means Succesful Transmission")
sleep(20)


