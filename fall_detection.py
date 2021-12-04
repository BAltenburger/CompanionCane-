import pandas as pd
from matplotlib import pyplot as plt
import time

def fall_detection(csv):
    return not is_heart_rate(csv) and accelerometer_fall(csv,1) and not is_force(csv)


def accelerometer_fall(csv, num):
    x = " accelerometer" + str(num) + "x"
    y = " accelerometer" + str(num) + "y"
    z = " accelerometer" + str(num) + "z"
    fall_check = False
    second_fall_check_count = 0
    timestamp = None
    index = 0
    
    for i in csv[z]:
        if 0<= i <= 1.5:
            fall_check = True
            timestamp = csv["time"][index]
        
            time.sleep(10)
            second_index = 0
            for x in range(0,49):
                if 0 <= csv[z][second_index - x] <= 1.5:
                    second_fall_check_count += 1
                second_index += 1
            index += 1

            

    if not(second_fall_check_count == 0) and fall_check == True:
        fall_check = True
        
    else:
        fall_check = False
        timestamp = None
        
    print(timestamp)
    return fall_check


def is_force(csv):
    for i in csv[" strain guage"]:
        if i == 0:
            return True
    return False

def is_heart_rate(csv):
    time.sleep(30)

    for i in range(len(csv[" HR"]) - 150, len(csv[" HR"])):
        if csv[" HR"][i] == 0:
            return False
    return True

df = pd.read_csv("data.csv", parse_dates = True)
print(fall_detection(df))



