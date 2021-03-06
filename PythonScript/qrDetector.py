#!/usr/bin/env python3
"""
Multi-threaded qr reader with pyzbar
"""
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
from threading import Thread
import cv2


#Variables
WEBCAM_RES_X = 480
WEBCAM_RES_y = 640
BWF_TOL = 150


#cv2.VideoCapture runs on its own thread
class WebcamStream:
    def __init__(self,src =0):
        #init cv stream
        self.stream =cv2.VideoCapture(src)
        self.stream.set(3,WEBCAM_RES_y)
        self.stream.set(4,WEBCAM_RES_X)
        self.stopped = False
        
        #read first frame from the stream
        self.ret, self.img = self.stream.read()
    
    def start(self):
        Thread(target = self.update, args=()).start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
                
            self.ret,self.img = self.stream.read()
            
    def read(self):
        return self.img
    
    def stop(self):
        print('releasing the camera')
        self.stream.stream.release()
        self.stopped = True

    #simplifed to just this for the moment to get the general alighment
    # Probabally need to revert to the larger version in order to get 
    # proper alignment        
    #######################################
    def decode(self, im):
        decodedObjects = pyzbar.decode(im)
        count = 0
        for obj in decodedObjects:
    #        print('Type : ',obj.type)
    #        print('Data : ', obj.data,'\n')
            count +=1
        if count != 0:
            print('Qr code found : ', count)
            return True
        else:
            return False
    #######################################


    
    def __del__(self):
        print('releasing the camera')
        self.stream.stream.release()
        
        


