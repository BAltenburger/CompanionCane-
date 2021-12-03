import pandas as pd
from matplotlib import pyplot as plt
import time

def fall_detection(csv):
    return accelerometer_fall(csv,1) and not is_force(csv) and not is_heart_rate(csv)


def accelerometer_fall(csv, num):
    x = " accelerometer" + str(num) + "x"
    y = " accelerometer" + str(num) + "y"
    z = " accelerometer" + str(num) + "z"
    index = 0
        
    for i in csv[x]:
        if float(i) == float(csv[y][index]) == float(csv[z][index]):
            return True
        index += 1

    return False

def is_force(csv1):
    i = -1
    while i < csv[" strain guage"].index:
        if csv["strain guage"][i-1] != 0:
            return False
        i += 1
    return True

def is_heart_rate(csv1):
    time.sleep(30)

    for i in range(len(csv[" HR"]) - 150, len(csv[" HR"])):
        if csv["HR"] != 0:
            return True
    return False

def hr_checker():
	counter = 0
	age = 19 #open(“user_age.txt”, ‘r’).read()
	for i in csv["time"]:
		if i > (220 - age) * 0.93:
			counter += 1
		if counter >= 150:
			return True
	return False

df = pd.read_csv("data.csv", parse_dates = True)
print(fall_detection(df))



