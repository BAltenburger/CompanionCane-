import serial
from datetime import datetime
import schedule
import emailsender
from sms import sms
import time
import pandas as pd
import graphing
from os.path import exists
import threading

schedule.every().day.at("21:59").do(graphing.plot_today)
schedule.every().day.at("22:00").do(emailsender.emaildaily)
schedule.every().monday.do(graphing.plot_week)
schedule.every().monday.do(emailsender.emailweek)

def check():  
    Cane_fall=False
    sc=0
    oc=0
    fg=0
    hr=0
    while thread1.is_alive():
        compressed=pd.read_csv("data.csv",chunksize=100000,parse_dates = True)
        csv=pd.concat(compressed)
        length=len(csv.index)
        l=length-1
        if Cane_fall:
            while l>length-600 and l>3:
                b2=csv.iloc[l][" accelerometer1x"]
                b1=csv.iloc[l-1]["accelerometer1x"]
                c2=csv.iloc[l][" accelerometer1y"]
                c1=csv.iloc[l-1][" accelerometer1y"]
                d2=csv.iloc[l][" accelerometer1z"]
                d1=csv.iloc[l-1][" accelerometer1z"]
                f=csv.iloc[l][" strain guage"]
                h=csv.iloc[l][" HR"]
                bm=b1-b2
                cm=c1-c2
                dm=d1-d2
                if bm<0.1 and cm<0.1 and dm<0.1:
                    sc+=1
                if b2<3:
                    oc+=1     
                if f>0.4:
                    fg+=1
                if h>40:
                    hr+=1
            if fg>100 or hr>100:
                Cane_fall=False
            elif (sc>499 and oc>499):
                graphing
                sms("Fall detected")
                emailsender.emailtool("Fall data")
            sc=0
            oc=0
            fg=0
            Cane_fall=False
        while l>3 and l>length-40:
            b2=csv.iloc[l][" accelerometer1x"]
            b1=csv.iloc[l-1][" accelerometer1x"]
            c2=csv.iloc[l][" accelerometer1y"]
            c1=csv.iloc[l-1][" accelerometer1y"]
            d2=csv.iloc[l][" accelerometer1z"]
            d1=csv.iloc[l-1][" accelerometer1z"]
            bm=b1-b2
            cm=c1-c2
            dm=d1-d2
            if not bm-cm==0:
                r1=(b1-c1)/(cm-bm)
            else:
                r1=0
            if not cm-dm==0:
                r2=(c1-d1)/(dm-cm)
            else:
                r2=0
            if r1<=1 and r2<=1:
                if (r1>0 and r2>0) or (b1==c1 and b1==d1):
                    print(l)
                    print("fall detected")
                    time.sleep(30)
                    Cane_fall=True
                    l-=40
            l-=1
        time.sleep(0.5)
        
def cane():
    arduino=serial.Serial('COM6',115200) #'COM6' will vary so check your bluetooth settings. Also Macbook ports are notated differently than windows
    filename="data.csv"
    if not exists(filename):
        open(filename,"w").write("time, HR, accelerometer1x, accelerometer1y, accelerometer1z, strain guage, accelerometer2x, accelerometer2y, accelerometer2z\n")
    samples=1728000
    file=open(filename,"a")
    line=0
    while line<samples:
        getData=str(arduino.readline())
        now=str(datetime.now())
        data=str(getData)[2:len(getData)-5]
        #print(data)
        file=open(filename, "a")
        file.write(now+","+data+"\n")
        file.close()
        line+=1
        schedule.run_pending()    
    arduino.close()

thread1=threading.Thread(target=cane)
thread2=threading.Thread(target=check)
thread1.start()
thread2.start()
