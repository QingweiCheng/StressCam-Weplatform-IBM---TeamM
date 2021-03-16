import change_device_info

def load_file(*arg):
    print("Reading value")
    for i in arg:
        if i == 'image':
            print("Reading image value")
            return change_device_info.read_image_value()
        elif i == 'device':
            print("Reading device value")
            return change_device_info.read_device_value()
        elif i == 'wiotp':
            print("Reading wiotp value")
            return change_device_info.read_wiotp_info()

device_info = load_file('device')
print(device_info['statusInterval'])