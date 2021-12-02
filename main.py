import serial
from datetime import datetime
import schedule
import emailsender
from sms import sms
import graphing
from os.path import exists

arduino = serial.Serial('COM4', 115200) #check bluetooth setting/more bluetooth options/coms and change the com# to the outgoing connection
filename = "data.csv"
if not exists(filename):
    open(filename, "w").write("time, HR, accelerometer1x, accelerometer1y, accelerometer1z, strain guage, accelerometer2x, accelerometer2y, accelerometer2z\n")
samples = 432000
file = open(filename, "a")
line = 0
    
while line < samples:
    getData = str(arduino.readline())
    now = str(datetime.now())
    data = str(getData)[2:len(getData)-5]
    print(data)
    file = open(filename, "a")
    file.write(now + ", " + data + "\n")
    file.close()
    line = line + 1
    if hr_checker:
        sms("Dangerous Heart Rate detected, Attention needed")
        graphing
        emailsender.emailtool("health data")
    if fall_detection:
        sms("Fall detected, Attention needed")
        graphing
        emailsender.emailtool("health data")
    schedule.every().day.at("22:00").do(emailsender.emaildaily())
    schedule.every.monday.do(emailsender.emailweek())
