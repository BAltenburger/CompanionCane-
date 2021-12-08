import serial
from datetime import datetime
import schedule
import emailsender
from sms import sms
import time
import pandas as pd
#import graphing
from os.path import exists
import threading

# schedule.every().day.at("21:59").do(graphing.plot_today)
# schedule.every().day.at("22:00").do(emailsender.emaildaily)
# schedule.every().monday.do(graphing.plot_week)
# schedule.every().monday.do(emailsender.emailweek)
# def count(count):
#     while count>0:
#         time.sleep(1)
#         print(count)
#         count-=1
def check():  
    Cane_fall=True
    Cane_fall2=False
    sc=0
    oc=0
    fg=0
    #hr=0
    index=26373
    # while thread1.is_alive():
    while True:
        compressed=pd.read_csv("data.csv",chunksize=100000,parse_dates = True)
        csv=pd.concat(compressed)
        length=len(csv.index)
        # l=length-1
        l=index+300
        if Cane_fall and not Cane_fall2:
            l3=l
            l2=index-300
            fc=0
            while l2<index:
                f=float(csv.iloc[l2][" strain guage"])
                if abs(f)>3:
                    fc+=1
                # if fc>50:
                #     l2+=300
                #     Cane_fall2=True  
                #     print("fall stage 1 cleared")
                l2+=1
            if fc>50:
                l2+=300
                print(fc)
                Cane_fall2=True  
                print("fall stage 1 cleared")
            if not Cane_fall2:
                print("fc:"+str(fc))
                Cane_fall=False
                print("fall cancelled")
            # else:
            #     time.sleep(15)
        if Cane_fall2 and Cane_fall and l>index:                
            while l>index and l>3:
                b2=csv.iloc[l][" accelerometer1x"]
                b1=csv.iloc[l-1][" accelerometer1x"]
                c2=csv.iloc[l][" accelerometer1y"]
                c1=csv.iloc[l-1][" accelerometer1y"]
                d2=csv.iloc[l][" accelerometer1z"]
                d1=csv.iloc[l-1][" accelerometer1z"]
                f=float(csv.iloc[l][" strain guage"])
                #h=csv.iloc[l][" HR"]
                bm=b1-b2
                cm=c1-c2
                dm=d1-d2
                th=0.15
                if bm<th and cm<th and dm<th:
                    sc+=1
                if b2<0.5:
                    oc+=1     
                if abs(f)>3.5:
                    fg+=1
                # if h>40:
                #     hr+=1
                # if fg>50: #or hr>100:
                #     Cane_fall=False
                #     l-=600
                #     print("fall detection cancelled2")
                l-=1
            if fg>50: #or hr>100:
                Cane_fall=False
                l-=600
                print("fall detection cancelled2")    
            print("fg:"+str(fg))
            print("oc:"+str(oc))
            print("sc:"+str(sc))
            if (sc>149 or oc>149) and Cane_fall:
                # graphing
                print("fall confirmed")
                # sms("Fall detected")
                # emailsender.emailtool("Fall data")
            elif not fg>50:
                print("fall detection cancelled3")
            sc=0
            oc=0
            fg=0
            Cane_fall=False
            Cane_fall2=False
        # while l>3: #and l>length-40:
        #     b2=csv.iloc[l][" accelerometer1x"]
        #     b1=csv.iloc[l-1][" accelerometer1x"]
        #     c2=csv.iloc[l][" accelerometer1y"]
        #     c1=csv.iloc[l-1][" accelerometer1y"]
        #     d2=csv.iloc[l][" accelerometer1z"]
        #     d1=csv.iloc[l-1][" accelerometer1z"]
        #     bm=b1-b2
        #     cm=c1-c2
        #     dm=d1-d2
        #     if not bm-cm==0:
        #         r1=(b1-c1)/(cm-bm)
        #     else:
        #         r1=0
        #     if not cm-dm==0:
        #         r2=(c1-d1)/(dm-cm)
        #     else:
        #         r2=0
        #     if r1<=1 and r2<=1:
        #         if (r1>0 and r2>0) or (b1==c1 and b1==d1):
        #             print(l)
        #             print("fall detected")
        #             index=l
        #             #Cane_fall=True
        #             l-=40
        #     l-=1
        # time.sleep(0.5)
        
def cane():
    arduino=serial.Serial('COM6',115200)
    filename="new_data.csv"
    if not exists(filename):
        open(filename,"w").write("time, HR, accelerometer1x, accelerometer1y, accelerometer1z, strain guage, accelerometer2x, accelerometer2y, accelerometer2z\n")
    samples=1728000
    file=open(filename,"a")
    line=0
    while line<samples:
        getData=str(arduino.readline())
        now=datetime.now()
        data=str(getData)[2:len(getData)-5]
        #print(data)
        file=open(filename, "a")
        file.write(now+","+data+"\n")
        file.close()
        line+=1
        schedule.run_pending()    
    arduino.close()

# thread1=threading.Thread(target=cane)
# thread2=threading.Thread(target=check)
# thread1.start()
# thread2.start()
check()
