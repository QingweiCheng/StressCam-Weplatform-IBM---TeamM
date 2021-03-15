from picamera import PiCamera
import datetime
import time
from time import sleep
from subprocess import run
from gpiozero import CPUTemperature

##import vakues from device_info file

def capture_image():
    print("Camera Opening")
    camera = PiCamera()  #Set camera parameters
    print("setting rotation")
    camera.rotation = 180
    print("setting resolution")
    camera.resolution = (init_values.get("imageResolutionX"),init_values.get("imageResolutionY)")) #set camera resolution to 2592x1944
    camera.framerate = init_values.get("imageFrameRate")
    print("setting date")
    currDate = datetime.datetime.now().strftime("%d_%m_%y") #Set variable currDate to the datetime the image is taken
    currTime = datetime.datetime.now().strftime("%H_%M_%S") #set variable currTime to the time the image is taken
    print("capturing image")
    camera.capture('/home/pi/images/' + currDate + '_' + currTime + init_values.get("imageFormat")) #name the image in the format of Y-M-D-h-m-s in jpg, bmp, png
    camera.close() # turn off camera to release the camera resourse
    #camera.stop_preview()
    print("Image Taken")
    sleep(5)


def resize_image(height = init_values.get("imageHeight"), width = init_values.get("imageWidth")):
    image_size = {
        "image_Height" : height,
        "image_Width" : width
    }
    print("Images Resized to", image_size.get("image_Width"),"x", image_size.get("image_Height"),"y")
    return image_size

def change_resolution(new_x_resolution = 2592,new_y_resolution = 1944):
    new_resolution={
    "imageResolutionX" : new_x_resolution,
    "imageResolutionY" : new_y_resolution
    }
    print("Resolution changed to:", new_resolution.get("imageResolutionX") ,"x", new_resolution.get("imageResolytionY") , "y") # set image resolution to the desire value pulled from web request's meta data
    return new_resolution

def new_interval(interval = init_values.get("statusInterval")):
    statusInterval = interval # convert received minute interval to seconds
    print("Interval Changed to:", statusInterval,"seconds") # display interval value in seconds
    return statusInterval

def run_script(script_type):
        print("Running Script"+ script_type)
        #if script extendtion is '.py', then use python3, else use super-user linux command
        if(script_type[-2:]=='py'):
            run(['python3', '/home/pi'+ script_type])
        else:
            run(['sudo','sh', '/home/pi'+ script_type])

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

def change_image_format(image_format = '.jpg'):
    if(image_format == '.jpg'):
        print("Format changed to:"+image_format)
    elif(image_format == '.png'):
        print("Format changed to:"+image_format)
    elif(image_format == '.bmp'):
        print("Format changed to:"+image_format)
    else:
        print("Incompatible format")
    init_values["imageFormat"] = image_format
    return init_values.get("imageFormat")

def publish_data():
    cpu = gpz.CPUTemperature()
        device_value = commands.Device(##put info from device_info value here)
        print("SensorData Published")
    # publish client event data using IBM Watson IoT PY SDK
        client.publishEvent("status","json", device_value.__dict__)


class Device:
    def __init__(self, device_ID, device_status, latitude, Longtitude):
        self.DEVICE_ID = device_ID
        self.DEVICE_STATUS = device_status
        self.LATITUDE = latitude
        self.LONGITUDE = Longtitude

