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

if not exists("data.csv"):
    file = open("data.csv","w")
    file.write("time, HR, accelerometer1x, accelerometer1y, accelerometer1z, strain gauge, accelerometer2x, accelerometer2y, accelerometer2z\n")
    file.close()
def scheduling():
    time.sleep(60)
    schedule.every().day.at("21:59").do(graphing.graphing())
    schedule.every().day.at("22:00").do(emailsender.emaildaily)
    schedule.every().monday.do(graphing.graphing())
    schedule.every().monday.do(emailsender.emailweek)
    
def check():  
    Cane_fall=False
    Cane_fall2=False
    sc=0
    oc=0
    fg=0
    index=0
    t=0
    while thread1.is_alive():
        compressed=pd.read_csv("data.csv",chunksize=100000,parse_dates = True)
        csv=pd.concat(compressed)
        length=len(csv.index)
        l=length-1
        if Cane_fall and not Cane_fall2:
            l3=l
            l2=index-50
            if l2<2:
                l2=2
            fc=0
            while l2<index:
                f=float(csv.iloc[l2][" strain gauge"])
                if abs(f)>3:
                    fc+=1
                l2+=1
            if fc>25:
                l2+=300
                print(fc)
                Cane_fall2=True  
                print("fall stage 1 cleared")
            if not Cane_fall2:
                print("fc:"+str(fc))
                Cane_fall=False
                print("fall cancelled")
        if Cane_fall2 and Cane_fall and l>l3:                
            while l>l3 and l>3 and t<15:
                b2=float(csv.iloc[l][" accelerometer1x"])
                b1=float(csv.iloc[l-1][" accelerometer1x"])
                c2=float(csv.iloc[l][" accelerometer1y"])
                c1=float(csv.iloc[l-1][" accelerometer1y"])
                d2=float(csv.iloc[l][" accelerometer1z"])
                d1=float(csv.iloc[l-1][" accelerometer1z"])
                f=float(csv.iloc[l][" strain gauge"])
                bm=abs(b1-b2)
                cm=abs(c1-c2)
                dm=abs(d1-d2)
                th=0.15
                if bm<th and cm<th and dm<th:
                    sc+=1
                if abs(float(b2))<5.2:
                    oc+=1     
                if abs(f)>3:
                    fg+=1
                l-=1
            time.sleep(0.5)
            t+=1
            print(t)
            print(fg)
            if fg>30:
                print("fall detection cancelled2")    
                print("fg:"+str(fg))
                print("oc:"+str(oc))
                print("sc:"+str(sc))
                sc=0
                oc=0
                fg=0
                t=0
                Cane_fall=False
                Cane_fall2=False
            elif (sc>99 or oc>99) and Cane_fall and t>14:
                graphing.graphing()
                print("fall confirmed")
                sms("Fall detected")
                emailsender.emailtool("Fall data")
                print("fg:"+str(fg))
                print("oc:"+str(oc))
                print("sc:"+str(sc))
                sc=0
                oc=0
                fg=0
                t=0
                Cane_fall=False
                Cane_fall2=False
            elif t>14:
                print("fall detection cancelled3")
                print("fg:"+str(fg))
                print("oc:"+str(oc))
                print("sc:"+str(sc))
                sc=0
                oc=0
                fg=0
                t=0
                Cane_fall=False
                Cane_fall2=False
        while l>3 and l>length-30 and not Cane_fall:
            b2=float(csv.iloc[l][" accelerometer1x"])
            b1=float(csv.iloc[l-1][" accelerometer1x"])
            c2=float(csv.iloc[l][" accelerometer1y"])
            c1=float(csv.iloc[l-1][" accelerometer1y"])
            d2=float(csv.iloc[l][" accelerometer1z"])
            d1=float(csv.iloc[l-1][" accelerometer1z"])
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
            r1=abs(r1)
            r2=abs(r2)
            if r1<=1 and r2<=1:
                if (r1>0 and r2>0) or (b1==c1 and b1==d1):
                    print(l)
                    print("fall detected")
                    index=l
                    Cane_fall=True
                    l-=40
            l-=1
        time.sleep(0.5)
        
def cane():
    arduino=serial.Serial('COM6',115200)
    filename="data.csv"
    samples=2000000
    file=open(filename,"a")
    line=0
    while line<samples:
        getData=str(arduino.readline())
        now=str(datetime.now())
        data=str(getData)[2:len(getData)-5]
        # print(data)
        file=open(filename, "a")
        file.write(now+","+data+"\n")
        file.close()
        line+=1
        schedule.run_pending()    
    arduino.close()

thread1=threading.Thread(target=cane)
thread2=threading.Thread(target=check)
thread3=threading.Thread(target=scheduling)
thread1.start()
time.sleep(1)
thread2.start()
thread3.start()
