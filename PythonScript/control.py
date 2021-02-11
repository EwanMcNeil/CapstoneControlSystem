from __future__ import print_function
import serial
import threading
import pyzbar.pyzbar as pyzbar
import cv2
import time 
import pyzbar.pyzbar as pyzbar
import numpy as np
from threading import Thread
import bluetooth, subprocess
from controlQR import WebcamStream,decode,draw_box, runQR




aligned = False
locked = False
retrieved = False

#Variables
WEBCAM_RES_X = 480
WEBCAM_RES_y = 640
BWF_TOL = 150
DroneQueue= []


##nearby devices is all the blue tooth devices around it
#using PyBluez to setup the bluetooth communcation 
#one function will constantly search for nearby drones and add them to the queue

def searchBlueDrones():
    nearby_devices = bluetooth.discover_devices(duration=4,lookup_names=True,
    flush_cache=True, lookup_class=False)

    for device in nearby_devices:

        #devies has the form (b'7C:94:2A:3D:F1:B3', 'HUAWEI P30 lite')
        #if () ##conditional statement for a drone in the system, if found start a comunication thread
        print(device)





#One communication thread per drone
def droneCommuncationThread():

    global connectedDrone
    ##set this up on the arduino
    name = "Drone"     # Device name
    addr = '7C:94:2A:3D:F1:B3'    # Device Address
    port = 1         # RFCOMM port
    passkey = "1111" # passkey of the device you want to connect


    #begining logic if we have a queue of drones (which we don't)
    #while(True):
       # if() ##conditional statment checking spot in the queue 
            # kill any "bluetooth-agent" process that is already running
        


    subprocess.call("kill -9 `pidof bluetooth-agent`",shell=True) # do we need to do this?

    # Start a new "bluetooth-agent" process where XXXX is the passkey
    status = subprocess.call("bluetooth-agent " + passkey + " &",shell=True)

    # Now, connect in the same way as always with PyBlueZ
    try:
        connectedDrone.connect((addr,port))
    except bluetooth.btcommon.BluetoothError as err:
        # Error handler TODO TODO 
        pass


    ##now the drone has been connected and we can communicate serially with it
    connectedDrone.recv(1024) # Buffer size


    # first message being sent is to land on the dock
    # in form LAND_DRONE#_DOCK#
    # Just assuming current dock # is one and name is one
    connectedDrone.send("LAND_"+ "1" + "_" + "1")





#Swap Sequence starts after the drone has landed.
def swapSequence():
    global connectedDrone

    #either through communcation with the drone or the pressure sensors prompts the operation
    #currently have the code for waiting for the bluetooth communcation

    landed = False
    try:
        while not landed:
            data = client_sock.recv(1024)
            if not data:
                break
            print("Received", data)
            if(data ==  "LAND_"+ "1" + "_" + "1"):
                landed = True
    except OSError:
            pass


    connectedDrone.close();
    ##After landed: connection is stopped because drone powers off 
    ## Telling the rotational microcontroller to start
    rotation.write(b"<ALIGNMENT_START>")

    def waitAlign():
        global aligned
        ## Loop for alighment confirmation 
        while not aligned:
            line = rotation.readline().decode('utf-8').rstrip()
            print(line)
            if line == "<ALIGNMENT_FINISHED>":
                aligned = True

    #QR code needs to be run within the main thread
    th = threading.Thread(target=waitAlign)
    th.start()


    runQR()
        
    #Telling the locking microcontroller to start
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


    ## now need to reconnect to the drone that has been repowered and tell it to takeoff


    connected = False

    while not connected:
        try:
            connectedDrone.connect((addr,port))
        except bluetooth.btcommon.BluetoothError as err:
            pass

    connectedDrone.send("Takeoff_"+ "1" + "_" + "1")

    connectedDrone.close()
    



    






# #Setting up the usb serial connections to the microcontrollers
# rotation = serial.Serial('/dev/tty.usbmodemFA131', 9600, timeout = 1)
# rotation.flush()

# locking = serial.Serial('/dev/ttyACM1', 9600, timeout = 1)
# locking.flush()

# arm = serial.Serial('/dev/ttyACM2', 9600, timeout = 1)
# arm.flush()


#declaring the global currently connected drone
connectedDrone = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
searchBlueDrones()
