#!/usr/bin/python3 -u
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from __future__ import print_function
import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
from gattlib import *
from threading import Event

class Requester(GATTRequester):
    def __init__(self, wakeup, *args):
        GATTRequester.__init__(self, *args)
        self.wakeup = wakeup


    def on_notification(self, handle, data):
        print("- notification on handle: {}\n".format(handle))
        self.wakeup.set()


class ReceiveNotification(object):
    def __init__(self, address):
        self.received = Event()
        self.requester = Requester(self.received, address, False)

        self.connect()
        self.wait_notification()

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK!")

    def wait_notification(self):
        print("\nThis is a bit tricky. You need to make your device to send\n"
              "some notification. I'll wait...")
        self.received.wait()


if __name__ == '__main__':

    service = DiscoveryService("hci0")
    devices = service.discover(2)

    droneMac = "unknown"


    for address, name in devices.items():
        print("name: {}, address: {}".format(name, address))
        if(name == "Drone_1"):
            droneMac = address

    print(droneMac)

    #uuid = "304af5d5-6b09-4402-8061-4d6f61d8ece3"

    ReceiveNotification(droneMac)

    print("Done.")
