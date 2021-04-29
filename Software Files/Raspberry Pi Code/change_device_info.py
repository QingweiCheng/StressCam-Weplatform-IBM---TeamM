import json


#read saved device info for value initialization
with open('/home/pi/device_info.json') as init_file:
    data = json.load(init_file)
    init_file.close()

#initalize info for command.py
def read_image_value():
    with open('/home/pi/device_info.json') as init_file:
        data = json.load(init_file)
        init_file.close()
    image_info = data['image_value']
    return image_info

def read_device_value():
    with open('/home/pi/device_info.json') as init_file:
        data = json.load(init_file)
        init_file.close()
    device_info = data['device_info']
    return device_info

def read_key_info():
    with open('/home/pi/device_info.json') as init_file:
        data = json.load(init_file)
        init_file.close()
    password_info = data['key']
    return password_info

#change device info
def change_device_info(**kwargs): #read in dict object
    for keys in kwargs: #iterate over all items inside the dict object
        for key in data['device_info']: # iterate over all items in device_info from device_info.json file
           if keys == key: #if there is a match then update the device_info.json file
                data['device_info'][key]= kwargs[keys]
                break
    #writeing the updated value into device_info.json file.
    with open('/home/pi/device_info.json','w') as user_file:
        json.dump(data,user_file,indent=4)
    user_file.close()

#change wiotp info
#This method follows the same logic as method "change_device_info"
def change_ibm_info(**kwargs):
    for keys in kwargs:
        for key in data['ibm_info']:
           if keys == key:
                data['ibm_info'][key]= kwargs[keys]
                break

    with open('/home/pi/device_info.json','w') as user_file:
        json.dump(data,user_file,indent=4)
    user_file.close()

#change image info
#This method follows the same logic as method "change_device_info"
def change_image_value(**kwargs):
    for keys in kwargs:
        for key in data['image_value']:
           if keys == key:
                data['image_value'][key]= kwargs[keys]
                break

    with open('/home/pi/device_info.json','w') as user_file:
        json.dump(data,user_file,indent=4)
    user_file.close()
