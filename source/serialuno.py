# -- coding: utf-8 --
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import time

def serialtransmit(array):
    port = "/dev/ttyUSB0"
    baud = 115200
    
    print("test")
    ser = serial.Serial(port=port, baudrate=baud, timeout=.1)
    
    try:
        print(ser.name)
    
        time.sleep(2)
        r = ser.read(6)
        print(r)
    
        for line in array:
            s = "{} {} {} {}\n".format(int(float(line[0])),int(float(line[1])),int(float(line[2])),int(float(line[3])))
            ser.write(bytes(s,'utf-8'))
            time.sleep(2)
    
            r = ser.readline()
            print(r)
    
    except Exception as e:
        print(e)
        pass
        ser.close()