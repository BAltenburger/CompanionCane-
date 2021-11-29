import serial
from datetime import datetime

arduino = serial.Serial('COM4', 115200) #check bluetooth setting/more bluetooth options/coms and change the com# to the output connection
filename = "analog-data.csv"
open(filename, "w").write("")
samples = 432000
file = open(filename, "a")
file.write("time, HR, accelerometer1x, accelerometer1y, accelerometer1z, accelerometer2x, accelerometer2y, accelerometer2z, strain guage\n")
line = 0
    
while line < samples:
    getData = str(arduino.readline())
    now = str(datetime.now())
    data = str(getData)[2:len(getData)]
    print(data)
    file = open(filename, "a")
    file.write(now + ", " + data + "\n")
    file.close()
    line = line + 1
