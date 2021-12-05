import pandas as pd
import datetime
from scipy.optimize import fsolve

def check():        
    stuff=pd.read_csv("test.csv", parse_dates = True)
    length=len(stuff.index)
    l=length-1
    print(l)
    if l>2:
        while l>2 and l>length-30:
            b2=stuff.iloc[l][" accelerometer1x"]
            b1=stuff.iloc[l-1][" accelerometer1x"]
            c2=stuff.iloc[l][" accelerometer1y"]
            c1=stuff.iloc[l-1][" accelerometer1y"]
            d2=stuff.iloc[l][" accelerometer1z"]
            d1=stuff.iloc[l-1][" accelerometer1z"]
            bm=b1-b2
            cm=c1-c2
            dm=d1-d2
            b=lambda x:bm*x+b1
            c=lambda x:cm*x+c1
            d=lambda x:dm*x+d1
            r1=fsolve(lambda x:b(x)-c(x),0.0)
            r2=fsolve(lambda x:c(x)-d(x),0.0)
            # print(r1)
            # print(r2)
            if r1<=1 and r2<=1:
                if (r1>0 and r2>0) or (b1==c1 and b1==d1):
                    print("fall detected")
                    return True
            l-=2
