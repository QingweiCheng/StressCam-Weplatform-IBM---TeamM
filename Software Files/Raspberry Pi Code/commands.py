from picamera import PiCamera
import datetime
from time import sleep
from subprocess import run
from gpiozero import CPUTemperature
from random import randrange
import change_device_info
##import values from device_info file
image_info = change_device_info.read_image_value()
device_info = change_device_info.read_device_value()

#This method will provide current device and image information 
def load_file(*arg): #argument(s) passed in here as a tuple
    print("Reading value")
    info = '' #initialize variable
    for i in arg:
        if i == 'image':
            print("Reading image value")
            info += f'Current Device Info: {change_device_info.read_image_value()}'
        elif i == 'device':
            print("Reading device value")
            info += f'\nCurrent Image Info: {change_device_info.read_device_value()}'
    return info #return info variable

#This method will take image and save the image inside images folder
def capture_image(currDate, currTime):
    image_info = change_device_info.read_image_value()
    print("Camera Opening")
    camera = PiCamera()  #Set camera parameters
    print("setting rotation")
    camera.rotation = 180
    print("setting resolution")
    camera.resolution = (image_info["imageResolutionX"],image_info["imageResolutionY"]) #set camera resolution to 2592x1944
    camera.framerate = image_info["imageFrameRate"]
    print("capturing image")
    camera.capture('/home/pi/images/' + currDate + '_' + currTime + image_info["imageFormat"]) #name the image in the format of Y-M-D-h-m-s in jpg, bmp, png
    camera.close() # turn off camera to release the camera resourse
    #camera.stop_preview()
    print("Image Taken")
    sleep(5)


#This method will resize the image
def resize_image(height = image_info["imageHeight"], width = image_info["imageWidth"]):
    image_size = {
        "imageWidth" : width,
        "imageHeight" : height
    }
    change_device_info.change_image_value(**image_size)
    print("Images Resized to", image_size["imageWidth"],"x", image_size["imageHeight"],"y")



#This method will change the resolution the next image being taken 
def change_resolution(new_x_resolution = image_info['imageResolutionX'],new_y_resolution = image_info['imageResolutionY']):
    new_resolution={
    "imageResolutionX" : new_x_resolution,
    "imageResolutionY" : new_y_resolution
    }
    change_device_info.change_image_value(**new_resolution)
    print("Resolution changed to:", new_resolution.get("imageResolutionX") ,"x", new_resolution.get("imageResolutionY") , "y") # set image resolution to the desire value pulled from web request's meta data


#This method will change the status update interval.
def new_interval(interval = device_info["statusInterval"]):
    statusInterval = {
        "statusInterval":interval # convert received minute interval to seconds
    }
    change_device_info.change_device_info(**statusInterval)
    print("Interval Changed to:", statusInterval,"seconds") # display interval value in seconds


#This method will run the desired script
def run_script(script_type):
        print("Running Script"+ script_type)
        #if script extendtion is '.py', then use python3, else use super-user linux command
        if(script_type[-2:]=='py'):
            run(['python3', '/home/pi/'+ script_type])
        else:
            run(['sudo','sh', '/home/pi/'+ script_type])


#This method will change camera operating schedule
def change_schedule(start_time, end_time):
    startTime = datetime.datetime.strptime(start_time,"%H:%M") # parse start time
    endTime = datetime.datetime.strptime(end_time,"%H:%M") # parse end time
    onTimeHours = endTime.hour - startTime.hour # calculate how many hours are on
    onTimeMin = endTime.minute - startTime.minute # calcualte how many minus are on
    #calculate off time hours and minuits
    # if minute vlaue is larger than zero, hour value need to be offset by 1.
    if(onTimeMin>0):
        offTimeHours = 23 - onTimeHours
        offTimeMin = 60- onTimeMin
    elif(onTimeMin == 0):
        offTimeHours = 24-onTimeHours
        offTimeMin = 0
    ## This is consfusing, the value of 'onTimeMin' an be smaller than 0?
    else: ## seems wrong
        offTimeHours = 24 - onTimeHours
        onTimeHours = onTimeHours-1
        onTimeMin = 60 - abs(onTimeMin)
        offTimeMin = 60 - onTimeMin
    # modify witttpi schedule
    f =  open('/home/pi/wittyPi/schedules/schedule.wpi','w')
    f.write('BEGIN   2015-08-01 '+ start_time+':00'+ '\n')
    f.write('END     2025-07-31 23:59:59'+ '\n')
    f.write('ON      H'+ str(onTimeHours) + ' M' + str(onTimeMin)+ '\n')
    f.write('OFF     H'+ str(offTimeHours)+ ' M' + str(offTimeMin))
    f.close


#This method will change the format of future image taken
def change_image_format(image_format = image_info['imageFormat']):
    new_image_format={
       "imageFormat":image_format
   }
    change_device_info.change_device_info(**new_image_format)
    if(image_format == '.jpg'):
        print("Format changed to:"+image_format)
    elif(image_format == '.png'):
        print("Format changed to:"+image_format)
    elif(image_format == '.bmp'):
        print("Format changed to:"+image_format)
    else:
        print("Incompatible format")


#This method will change the image frame rate
def change_frame_rate(frame_rate = image_info['imageFrameRate']):
    new_frame_rate={
       "imageFrameRate":frame_rate
   }
    change_device_info.change_image_value(**new_frame_rate)
    print("Frame rate changed to:",frame_rate)


#This method will return information of image and camera itself
def publish_data(currDate, currTime, waterStressLevel,witty_temp =randrange(30,40) ):
    device_info = change_device_info.read_device_value()
    cpu = CPUTemperature()
    data = {
    "DEVICE_ID": device_info['deviceId'],
    "LATITUDE": device_info['cameraLatitude'],
    "LONGITUDE": device_info['cameraLongitude'],
    "WATER_STRESS_LEVEL":waterStressLevel,
    "WITTYPI_TEMPERATURE": witty_temp, #wittyPiTemp,
    "CPU_TEMPERATURE": cpu.temperature,
    "DATE_1":currDate,
    "TIME_1":currTime
    }
    print(data)
    print("SensorData Published")
    return data


