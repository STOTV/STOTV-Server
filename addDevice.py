#!/usr/bin/env python
import server
import os

server.db.create_all();
imei=int(input("What is the RockBLOCK's IMEI Number: "))
deviceName=input("What do you want the device to be called publicly? ")
returnName=input("What name is to be used in case of recovery? ")
returnAddr1=input("What Address is to be used in case of recovery? Line 1: ")
returnAddr2=input("What Address is to be used in case of recovery? Line 2: ")
device=server.Device(imei,deviceName,returnName,returnAddr1,returnAddr2)
server.db.session.add(device)
server.db.session.commit()
