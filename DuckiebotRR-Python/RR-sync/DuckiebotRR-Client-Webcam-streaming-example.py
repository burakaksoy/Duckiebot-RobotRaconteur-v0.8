#Simple example Robot Raconteur webcam client
#This program will show a live streamed image from
#the webcams.  Because Python is a slow language
#the framerate is low...

from RobotRaconteur.Client import *

import time
import thread
import numpy
import cv2
import sys

#Function to take the data structure returned from the Webcam service
#and convert it to an OpenCV array
def WebcamImageToMat(image):
    frame2=image.data.reshape([image.height, image.width, 3], order='C')
    return frame2

current_frame=None
finish_time = 0

def main():
    is_view = True
    url='rr+tcp://192.168.43.141:2355?service=Webcam'
    if (len(sys.argv)>=2):
        url=sys.argv[1]

    #Startup, connect, and pull out the camera from the objref
    RRN.UseNumPy=True
    c_host=RRN.ConnectService(url)

    c=c_host.get_Webcams(0)

    #Connect the pipe FrameStream to get the PipeEndpoint p
    p=c.FrameStream.Connect(-1)

    #Set the callback for when a new pipe packet is received to the
    #new_frame function
    p.PacketReceivedEvent+=new_frame
    try:
        c.StartStreaming()
    except: pass

    if (is_view):
        cv2.namedWindow("Image")

    while True:
        #Just loop resetting the frame
        #This is not ideal but good enough for demonstration

        if (not current_frame is None):
            if (is_view):
                cv2.imshow("Image",current_frame)
            else:            
                a = 1
        if cv2.waitKey(50)!=-1:
            break
    cv2.destroyAllWindows()

    p.Close()
    c.StopStreaming()

#This function is called when a new pipe packet arrives
def new_frame(pipe_ep):
    global current_frame
    global finish_time
    start_time = time.time()
    #Loop to get the newest frame
    while (pipe_ep.Available > 0):
        #Receive the packet
        image=pipe_ep.ReceivePacket()
        #Convert the packet to an image and set the global variable
        current_frame=WebcamImageToMat(image)
    print(str(1.0/(start_time - finish_time)))
    finish_time = time.time()
if __name__ == '__main__':
    main()
