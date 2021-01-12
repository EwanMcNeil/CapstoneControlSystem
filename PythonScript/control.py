import serial
import qrDetector
from qrDetector import WebcamStream
import threading
import cv2
import time ##might not need these double imports


aligned = False
locked = False
retrieved = False



def qrAlignment():
    camStream = WebcamStream()
    counter =0
    print(" QRCode detector pyzbar multithreaded ")
    camStream.start()
    while True:
        img = camStream.read()
        mask = cv2.inRange(img,(0,0,0),( BWF_TOL, BWF_TOL, BWF_TOL))
        thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        bw_img = 255-thresholded # black-in-white
        foundQR = decode(bw_img)

        if foundQR is True:
            aligned = True

    
        
    #cap.release()#close camera
    del camStream
    cv2.destroyAllWindows()
    print('exiting program')



if __name__ == '__main__':

    #Setting up the usb serial connections to the microcontrollers
    rotation = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
    rotation.flush()

    locking = serial.Serial('/dev/ttyACM1', 9600, timeout = 1)
    locking.flush()

    arm = serial.Serial('/dev/ttyACM2', 9600, timeout = 1)
    arm.flush()


    ## Current code is setup to wait for the next call in the sequence.
    ## Assuming drone has landed


    ## Telling the rotational microcontroller to start
    rotation.write(b"<ALIGNMENT_START>")
    aligned = False

    th = threading.Thread(target=qrAlignment)
  


    ## Loop for alighment confirmation 
    while not aligned:
        line = rotation.readline().decode('utf-8').rstrip()

        if line is "ALIGNMENT_FINISHED":
            aligned = True
    


    ##Telling the locking microcontroller to start
    locking.write(b"<LOCKING_START>")
    locked = False



    while not locked:
        line = locking.readline().decode('utf-8').rstrip()

        if line is "LOCKING_FINISHED":
            aligned = True



    arm.write(b"<RETREIVE_START>")
    retrieved = False

    while not retrieved:
        line = arm.readline().decode('utf-8').rstrip()

        if line is "RETREIVE_FINISHED":
            retrieved = True

    ## we might need to setup sleeping in this and error detection



