import sys

sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
from gattlib import * 

service = DiscoveryService("hci0")
devices = service.discover(2)

droneMac = "unknown"

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))
    if(name == "Drone_1"):
        droneMac = address
        

    
print(droneMac)  



req = GATTRequester(droneMac)


data = req.read_by_uuid("304af5d5-6b09-4402-8061-4d6f61d8ece3")

print("bytes recieved:", end = ' ')
for b in data:
	print(hex(ord(b)), end = ' ')
print("")


