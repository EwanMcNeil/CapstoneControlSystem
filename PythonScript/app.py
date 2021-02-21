# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/
import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import os
import asyncio
import platform
import threading
from datetime import datetime
from typing import Callable, Any
import serial
import time 


from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from SwapDockUI import Ui_MainWindow



from aioconsole import ainput
from bleak import BleakClient, discover

#editing from vi
root_path = os.environ["HOME"]

selected_device = []

startup = False
message = " "
messageFlag = False
uiCreation = False

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
       print("ran")
      # self.action_Exit.triggered.connect(self.close)
       #self.action_Find_Replace.triggered.connect(self.findAndReplace)
      # self.action_About.triggered.connect(self.about)

    def findAndReplace(self):
        dialog = FindReplaceDialog(self)
        dialog.exec()

    def about(self):
        QMessageBox.about(
            self,
            "About Sample Editor",
            "<p>A sample text editor app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",
        )



class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/find_replace.ui", self)




class Connection:
    
    client: BleakClient = None
    
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        read_characteristic: str,
        write_characteristic: str,
    ):
        self.loop = loop
        self.read_characteristic = read_characteristic
        self.write_characteristic = write_characteristic

        self.last_packet_time = datetime.now()
        self.connected = False
        self.connected_device = None

        self.rx_data = []
        self.rx_timestamps = []
        self.rx_delays = []

    async def on_disconnect(self, client: BleakClient):
        #removingfuture:asyncio.Future because it is not being used

        self.connected = False
        # Put code here to handle what happens on disconnet.
        #on disconnected we start searching again
        self.select_device()
        print(f"Disconnected from {self.connected_device.name}!")

    async def cleanup(self):
        if self.client:
            await self.client.stop_notify(read_characteristic)
            await self.client.disconnect()

    async def manager(self):
        print("Starting connection manager.")
        while True:
            if self.client:
                await self.connect()
            else:
                await self.select_device()
                await asyncio.sleep(15.0, loop=loop)       

    async def connect(self):
        if self.connected:
            return
        try:
            await self.client.connect()
            self.connected = await self.client.is_connected()
            if self.connected:
                print(F"Connected to {self.connected_device.name}")
                self.client.set_disconnected_callback(self.on_disconnect)
                await self.client.start_notify(
                    self.read_characteristic, self.notification_handler,
                )
                while True:
                    if not self.connected:
                        break
                    await asyncio.sleep(3.0, loop=loop)
            else:
                print(f"Failed to connect to {self.connected_device.name}")
        except Exception as e:
            print(e)

    async def select_device(self):
        print("Bluetooh LE hardware warming up...")
        await asyncio.sleep(2.0, loop=loop) # Wait for BLE to initialize.





        devices = await discover()
        response = -1;

        while(response == -1):
                print("Searching for drone: ")
                for i, device in enumerate(devices):
                    if(device.name == "Drone_1"):
                     response = i
             
                if(response == -1):
                   await asyncio.sleep(5,loop = loop)
                   devices = await discover()
                
        print(f"Connecting to {devices[response].name}")
        self.connected_device = devices[response]
        self.client = BleakClient(devices[response].address, loop=self.loop)


    def record_time_info(self):
        present_time = datetime.now()
        self.rx_timestamps.append(present_time)
        self.rx_delays.append((present_time - self.last_packet_time).microseconds)
        self.last_packet_time = present_time

    def clear_lists(self):
        self.rx_data.clear()
        self.rx_delays.clear()
        self.rx_timestamps.clear()
        
        

    def notification_handler(self, sender: str, data: Any):
        self.rx_data.append(int.from_bytes(data, byteorder="big"))
        self.record_time_info()
        print("notifed")
        print(int.from_bytes(data, byteorder="big"))
        droneMessage = int.from_bytes(data, byteorder="big")

	    #zero indicates drone has started connection
        global message
        global messageFlag
        if(droneMessage == 0):
            print("recieved 0")
            message = "LAND_DRONE"
            messageFlag = True

           

	    #one indicates the drone has landed 
        # After which we check for alignment 
        # once achieved send message to turn off lights 	
        if(droneMessage == 1):
            print("recieved 1")
            check = waitAlign()
            if(check == 1):
                message = "ALIGNED_DRONE"
                messageFlag = True
           
                  

 

#############
# Loops
#############

# #Setting up the usb serial connections to the microcontrollers
rotation = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
rotation.flush()

# locking = serial.Serial('/dev/ttyACM1', 9600, timeout = 1)
# locking.flush()

# arm = serial.Serial('/dev/ttyACM2', 9600, timeout = 1)
# arm.flush()

#this will tell all the microcontrollers at different stages what to do


def waitAlign():
    #telling microcontroller to start alignment checking 
    rotation.write(b"<ALIGNMENT_START>")
    aligned = False

    #waiting for postive aligment to procede to next step
    while not aligned:
        line = rotation.readline().decode('utf-8').rstrip()
        print(line)
        if line ==  "<ALIGNMENT_FINISHED>":
            aligned = True

    return 1;





async def writing_handler(connection: Connection,message):
    print("writing handler")
    bytes_to_send = bytearray(map(ord, message))
    await connection.client.write_gatt_char(write_characteristic, bytes_to_send)

async def user_console_manager(connection: Connection):
    global message
    global messageFlag
    global messageSem
    global startup
    while True:
        if connection.client and connection.connected:
            print(1)
            if(startup):
               if(messageFlag):
                    print(2)
               
                    print("SENDING: ")
                    print(message)
                
                    bytes_to_send = bytearray(map(ord, message))
                    await connection.client.write_gatt_char(write_characteristic, bytes_to_send)
                    messageFlag = False
               else:
                  print("on await")
                  await asyncio.sleep(2.0, loop=loop)

            else:
                print(3)
                firstmessage = "CONNECTED"
                bytes_to_send = bytearray(map(ord, firstmessage))
                await connection.client.write_gatt_char(write_characteristic, bytes_to_send)
                startup = True
        else:
            await asyncio.sleep(2.0, loop=loop)


async def main(connection: Connection):
    global startup
    global message
    global messageFlag
    while True:
        if connection.client and connection.connected:
            if(startup):
              if(messageFlag):
                    print("writing handler")
                    bytes_to_send = bytearray(map(ord, message))
                    await connection.client.write_gatt_char(write_characteristic, bytes_to_send)
                    messageFlag = False
              await asyncio.sleep(5)
            else:
              firstmessage = "CONNECTED"
              bytes_to_send = bytearray(map(ord, firstmessage))
              await connection.client.write_gatt_char(write_characteristic, bytes_to_send)
              startup = True
        else:
         await asyncio.sleep(2.0, loop=loop)

#############
# App Main
#############
read_characteristic = "00001143-0000-1000-8000-00805f9b34fb"
write_characteristic = "00001142-0000-1000-8000-00805f9b34fb"
exec 

async def UI_thread():
    global uiCreation
    if(not uiCreation):
        print("STARTED UI")
        uiCreation = True
        app = QApplication(sys.argv)
        win = Window()
        win.show()
        app.exec()
        #sys.exit(app.exec())
    else:
        await asyncio.sleep(5.0, loop=loop)



if __name__ == "__main__":
   
    
    # Create the event loop.
    loop = asyncio.get_event_loop()

   # UITask = asyncio.create_task(UI_thread())
    asyncio.to_thread(UI_thread())
  

    connection = Connection(
        loop, read_characteristic, write_characteristic
    )
    try:
        print("HELLO FROM DA LOOP")
        asyncio.ensure_future(connection.manager())
        #asyncio.ensure_future(UI_thread())
        
        #asyncio.ensure_future(user_console_manager(connection))
        asyncio.ensure_future(main(connection))
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(connection.cleanup())
    