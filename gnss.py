#!/usr/bin/python

import time

from websocket import create_connection

from pynmeagps import NMEAReader
from pyrtcm import RTCMReader

import serial

print("Init serial port")
serial_port = serial.Serial(
    port="/dev/ttyUSB1",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
time.sleep(1)

ws = create_connection("ws://192.168.1.1:80/ws")
print("Send 'Start'")
ws.send("Start")

try:
    while True:
        rtcm = ws.recv()
        # print("> RTCM '%s'" % rtcm)
        serial_port.write(rtcm)
        # try:
        # rtcmParsed = RTCMReader.parse(rtcm)
        # print(rtcmParsed)
        # except:
        # print("Could not parse RTCM")

        if (serial_port.in_waiting >= 1):
            got = serial_port.readline()
            # print(got)
            try:
                nmeaParsed = NMEAReader.parse(got)
                print(nmeaParsed)
                if (nmeaParsed.msgID == "RMC"):
                    print(str(nmeaParsed.lat) + "!" + str(nmeaParsed.lon))
                    f = open("latlon.txt", "w")
                    f.write(str(nmeaParsed.lat) + "," + str(nmeaParsed.lon))
                    f.close()
                # print("< GNSS '%s'" % got)
            except:
                print("Could not parse NMEA")



except KeyboardInterrupt:
    print("Exit")

except Exception as exception_error:
    print("Exception")
    print("Error: " + str(exception_error))

finally:
    ws.close()
    serial_port.close()
    pass