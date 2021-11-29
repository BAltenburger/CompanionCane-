import serial
from datetime import datetime

arduino = serial.Serial('COM4', 115200)
filename = "analog-data.csv"
open(filename, "w").write("")
print('Arduino connection:working')
samples = 432000
file = open(filename, "a")
file.write("time, HR, accelerometer1x, accelerometer1y, accelerometer1z, accelerometer2x, accelerometer2y, accelerometer2z, strain guage\n")
line = 0
def cane_status():
    if(not arduino.available()):
        return False;
    
    
while line < samples:
    getData = str(arduino.readline())
    now = str(datetime.now())
    data = str(getData)[2:len(getData)-5]
    print(data)
    file = open(filename, "a")
    file.write(now + ", " + data + "\n")
    file.close()
    line = line + 1
