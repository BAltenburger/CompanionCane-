import pandas as pd
import time

def check():  
    while thread1.is_alive():
        stuff=pd.read_csv("test.csv",parse_dates = True)
        length=len(stuff.index)
        l=length-1
        while l>3 and l>length-40:
            b2=stuff.iloc[l][" accelerometer1x"]
            b1=stuff.iloc[l-1][" accelerometer1x"]
            c2=stuff.iloc[l][" accelerometer1y"]
            c1=stuff.iloc[l-1][" accelerometer1y"]
            d2=stuff.iloc[l][" accelerometer1z"]
            d1=stuff.iloc[l-1][" accelerometer1z"]
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
                    time.sleep(1.5)
                    l-=40
            l-=1
        time.sleep(0.5)
