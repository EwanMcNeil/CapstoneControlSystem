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
    
    def __del__(self):
        print('releasing the camera')
        self.stream.stream.release()
        
        

        

