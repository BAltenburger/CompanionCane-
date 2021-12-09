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
    Cane_fall2=False
    stillcounter=0
    orientationcounter=0
    forcegauge=0
    indexoffall=0
    while thread1.is_alive():
        compressed=pd.read_csv("data.csv",chunksize=100000,parse_dates = True)
        csv=pd.concat(compressed)
        length=len(csv.index)
        l=length-1
        if Cane_fall and not Cane_fall2:
            l3=l
            l2=index-100
            if l2<2:
                l2=2
            forcecounter=0
            while l2<indexoffall:
                f=float(csv.iloc[l2][" strain guage"])
                if abs(f)>3:
                    forcecounter+=1
                # if forcecounter>19:
                #     l2+=300
                #     Cane_fall2=True  
                #     print("fall stage 1 cleared")
                l2+=1
            if forcecounter>19:
                l2+=300
                print("fc:"+str(forcecounter))
                Cane_fall2=True  
                print("fall stage 1 cleared")
            if not Cane_fall2:
                print("fc:"+str(forcecounter))
                Cane_fall=False
                print("fall cancelled")
            else:
                print("waiting 15 seconds")
                time.sleep(15)
        if Cane_fall2 and Cane_fall and l>l3:                
            while l>l3 and l>3:
                b2=float(csv.iloc[l][" accelerometer1x"])
                b1=float(csv.iloc[l-1][" accelerometer1x"])
                c2=float(csv.iloc[l][" accelerometer1y"])
                c1=float(csv.iloc[l-1][" accelerometer1y"])
                d2=float(csv.iloc[l][" accelerometer1z"])
                d1=float(csv.iloc[l-1][" accelerometer1z"])
                f=float(csv.iloc[l][" strain guage"])
                bm=abs(b1-b2)
                cm=abs(c1-c2)
                dm=abs(d1-d2)
                th=0.15
                if bm<th and cm<th and dm<th:
                    stillcounter+=1
                if abs(float(b2))<5.2:
                    orientationcounter+=1     
                if abs(f)>3:
                    forcegauge+=1
                # if fg>50: #or hr>100:
                #     Cane_fall=False
                #     l-=600
                #     print("fall detection cancelled2")
                l-=1
            if forcegauge>40: #or hr>100:
                Cane_fall=False
                print("fall detection cancelled2")    
            print("fg:"+str(fg))
            print("oc:"+str(oc))
            print("sc:"+str(sc))
            if (stillcounter>99 or orientationcounter>99) and Cane_fall:
                graphing
                print("fall confirmed")
                sms("Fall detected")
                emailsender.emailtool("Fall data")
            elif not forcegauge>50:
                print("fall detection cancelled3")
            stillcounter=0
            orientationcounter=0
            forcegauge=0
            Cane_fall=False
            Cane_fall2=False
        while l>3 and l>length-150 and not Cane_fall:
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
    if not exists(filename):
        open(filename,"w").write("time, HR, accelerometer1x, accelerometer1y, accelerometer1z, strain guage, accelerometer2x, accelerometer2y, accelerometer2z\n")
    samples=1728000
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
thread1.start()
thread2.start()
