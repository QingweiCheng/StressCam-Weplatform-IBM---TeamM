import commands
import datetime

def commandProcessor(cmd):

    command = cmd.data['CommandType']

    # print recieved command
    print("Command received: %s" % command)

   # if command is take image
    if command == "takeImage":
        currDate = datetime.datetime.now().strftime("%d_%m_%y")
       	currTime = datetime.datetime.now().strftime("%H_%M_%S")
        commands.capture_image(currDate,currTime)

    # if command is resize image
    if command == "resizeImage" and int(cmd.data['Height'])<=1944 and int(cmd.data['Width'])<=2592:
        commands.resize_image(int(cmd.data['Height']), int(cmd.data['Width']))
    else:
        print("Images not resized, size too large")

    #if command is to change resolution
    if(command == "changeResolution"):
        commands.change_resolution(int(cmd.data['imageResolutionX']), int(cmd.data['imageResolutionY']))

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
        commands.change_frame_rate(int(cmd.data['frames']))
        print("Frame Rate changed to:", int(cmd.data['frames']))#range(10fps-30fps)

    # if command is send data
    if(command == "sendData"):
        commands.publish_data()
        
