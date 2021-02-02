# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/
import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import os
import asyncio
import platform
import threading
from datetime import datetime
from typing import Callable, Any

from aioconsole import ainput
from bleak import BleakClient, discover


root_path = os.environ["HOME"]

selected_device = []

startup = False
message = " "
messageFlag = False
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

    def on_disconnect(self, client: BleakClient, future: asyncio.Future):
        self.connected = False
        # Put code here to handle what happens on disconnet.
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

        print("Please select device: ")
        for i, device in enumerate(devices):
            print(f"{i}: {device.name}")

        response = -1
        while True:
            response = await ainput("Select device: ")
            try:
                response = int(response.strip())
            except:
                print("Please make valid selection.")
            
            if response > -1 and response < len(devices):
                break
            else:
                print("Please make valid selection.")

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
        if(droneMessage == 1):
            print("recieved 1")
            message = "TAKEOFF_DRONE"
            messageFlag = True
           
                  

 

#############
# Loops
#############
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
        # YOUR APP CODE WOULD GO HERE.
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

if __name__ == "__main__":

    # Create the event loop.
    loop = asyncio.get_event_loop()

    connection = Connection(
        loop, read_characteristic, write_characteristic
    )
    try:
        asyncio.ensure_future(connection.manager())
        #asyncio.ensure_future(user_console_manager(connection))
        asyncio.ensure_future(main(connection))
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(connection.cleanup())