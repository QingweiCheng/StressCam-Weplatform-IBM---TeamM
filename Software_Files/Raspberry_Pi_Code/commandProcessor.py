from gpiozero.devices import Device
import commands
import wiotp.sdk.device

def commandProcessor(cmd):

    command = cmd.data['CommandType']

    # print recieved command
    print("Command received: %s" % command)

    if(command == "changeResolution"):
        commands.change_resolution(int(cmd.data['imageResolutionX']), int(cmd.data['imageResolutionY']))

    # if command is take image
    if command == "takeImage":
        commands.capture_image()

    # if command is resize image
    if command == "resizeImage" and int(cmd.data['Height'])<=1944 and int(cmd.data['Width'])<=2592:
        commands.resize_image(int(cmd.data['Height']), int(cmd.data['Width']))
    else:
        print("Images not resized, size too large")

    # if command is change send interval
    # Web page shows button to change status update interval value in minuits 
    #How often the RPI sends data back 
    if(command == "changeSendInterval"):
        commands.new_interval(int(cmd.data['Interval'])*60)

    # if command is run script
    if(command == "runScript"):
        commands.run_script(cmd.data['scriptType']) # scriptType -- meta data send from the web page. See more in /Web Plateform Design Files/Commands.html

    #if command is change schedule
    if(command == "changeSchedule"):
        print("changeSchedule")
        commands.change_schedule(cmd.data['startTime'], cmd.data['endTime'])    

    # if command is image format
    if(command == "imageFormat"):
        print("imageFormat") # JPG or PNG or BMP
        commands.change_image_format(cmd.data['imageFormat'])

    # if command is change frames
    if(command == "changeFrames"):
        int(cmd.data['frames'])
        print("Frame Rate changed to:", int(cmd.data['frames'])#range(10fps-30fps)

    # if command is send data
    if(command == "sendData"):
        command.publish_data()

        
