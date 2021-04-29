import json

#read saved device info 
with open('/home/pi/device_info.json') as init_file:
    data = json.load(init_file)
init_file.close()

#initalize info for command.py
def read_image_value():
    image_info = data['image_value']
    return image_info

def read_device_value():
    device_info = data['device_info']
    return device_info

def read_wiotp_info():
    wiotp_info = data['wiotp_info']
    return wiotp_info

#change device info
def change_device_info(**kwargs):
    for keys in kwargs:
        for key in data['device_info']:
           if keys == key:
                data['device_info'][key]= kwargs[keys]
                break

    with open('/home/pi/device_info.json','w') as user_file:
        json.dump(data,user_file,indent=4)
    user_file.close()

#change wiotp info
def change_wiotp_info(**kwargs):
    for keys in kwargs:
        for key in data['wiotp_info']:
           if keys == key:
                data['wiotp_info'][key]= kwargs[keys]
                break

    with open('/home/pi/device_info.json','w') as user_file:
        json.dump(data,user_file,indent=4)
    user_file.close()

#change image info
def change_image_value(**kwargs):    
    for keys in kwargs:
        for key in data['image_value']:
           if keys == key:
                data['image_value'][key]= kwargs[keys]
                break

    with open('/home/pi/device_info.json','w') as user_file:
        json.dump(data,user_file,indent=4)
    user_file.close()
