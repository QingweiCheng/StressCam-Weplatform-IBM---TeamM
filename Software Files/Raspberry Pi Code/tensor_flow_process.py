from sys import path
path.insert(0,"/usr/local/lib/python3.7/dist-packages/tensorflow_core/lite/python")
path.insert(0,"/usr/local/lib/python3.7/dist-packages/skimages")
from PIL import Image
from skimage.io import imread #read images
from skimage.io import imsave
from skimage.transform import resize #resize images
import lite as tflite
import numpy as np #modify arrays
#from keras.models import load_model # load pretrained models
from time import sleep

def ml_process(imagename):
    #im = imread('/home/pi/images/'+currDate+currTime+imageFormat)
    #Uncomment the above line to use the ML model on the taken image
    file = f'/home/pi/Pictures/{imagename}' # set 'file' to image directory
    im = Image.open(f'{file}')
    width,height = im.size
    if width != 200 & height !=200:
        im = imread(f'{file}')
        print("resizing image")
        im = resize(im,(200,200)) #Model was trained on 200x200 images
    else:
        im = imread(f'{file}')
    # Load TFLite model and allocate tensors.
    print("allocating tensors")
    interpreter = tflite.Interpreter(model_path="/home/pi/converted_model.tflite")
    interpreter.allocate_tensors()
    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    Xtest = np.array(im, dtype = np.float32)

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
    #Log file
    f =  open('/home/pi/waterStressLog.txt','a')
    #f.write(str(currDate)+str(currTime)+ " : " + str(waterStressLevel)+"\n")
    f.write(f"{imagename} : Water Stress Level:" + str(waterStressLevel)+","+str('%.2f'%percentConfident)+"% Confident"+"\n")
    f.close
    print(imagename)
    print("Water Stress Level", waterStressLevel)
    print("Percent Confident", '%.2f' % percentConfident)
    return waterStressLevel
