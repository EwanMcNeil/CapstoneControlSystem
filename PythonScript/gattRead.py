#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from __future__ import print_function

import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
from gattlib import *


class Reader(object):
    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.connect()
        self.request_data()

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK!")

    def request_data(self):
        data = self.requester.read_by_uuid("00001144-0000-1000-8000-00805f9b34fb")[0]

        print("bytes received:", end=' ')
        for b in data:
            print(hex(ord(b)), end=' ')
        print("")


if __name__ == '__main__':
    service = DiscoveryService("hci0")
    devices = service.discover(2)

    droneMac = "unknown"


    for address, name in devices.items():
        print("name: {}, address: {}".format(name, address))
        if(name == "Drone_1"):
            droneMac = address

    print(droneMac)


    Reader(droneMac)
    print("Done.")