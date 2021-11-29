import email_code  # name will depend on what the .py file for email is called
import pandas as pd
from matplotlib import pyplot as plt
import datetime
from collections import Counter

"""
time	heart rate	accelerometer1x	accelerometer1y	accelerometer1z	accelerometer1z	accelrometer2x	accelerometer2y	accelerometer2z	strain gauge

"""


def plot_today(heart_rate):
    # plots the data for today
    now = datetime.date.today()
    end_of_day = now - datetime.timedelta(hours=24)
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    end_of_day = end_of_day.strftime("%d/%m/%Y %H:%M:%S")

    heart_rate = heart_rate[(heart_rate['time'] > end_of_day) & (heart_rate['time'] < now)]
    plt.plot(heart_rate["time"], heart_rate["HR"])
    plt.xlabel("Time")
    plt.ylabel("Heart Rate")
    plt.title("Heart Rate Data over Time")
    plt.savefig("daily_time_heart_rate.png")


def plot_week(heart_rate):
    # plots the data for the week
    now = datetime.date.today()
    end_of_week = now - datetime.timedelta(hours=168)
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    end_of_week = end_of_week.strftime("%d/%m/%Y %H:%M:%S")

    heart_rate = heart_rate[(heart_rate['time'] > end_of_week) & (heart_rate['time'] < now)]
    plt.plot(heart_rate["time"], heart_rate["HR"])
    plt.xlabel("Time")
    plt.ylabel("Heart Rate")
    plt.title("Heart Rate Data over Time")
    plt.savefig("weekly_heart_rate.png")


def heart_rate_graphing(heart_rate, filename):

    # plots the all time heart rate data over time
    # print(heart_rate)
    plt.plot(heart_rate["time"], heart_rate["HR"])
    plt.xlabel("Time")
    plt.ylabel("Heart Rate")
    plt.title("Heart Rate Data over Time")
    plt.savefig("all_time_heart_rate.png")

    plot_today(heart_rate)
    plot_week(heart_rate)

    # checks to see if there are irregularities
    age = 19                 # open(“user_age.txt”, ‘r’).read()
    level = []
    for i in heart_rate["HR"]:
        if i >= (220 - age) * 0.93:
            level.append("Dangerous")
        elif ((220 - age) * 0.77) < i < ((220 - age) * 0.93):
            level.append("High")
        elif ((220 - age) * .64) < i < ((220 - age) * 0.77):
            level.append("Medium")
        else:
            level.append("Normal")

    heart_rate['Level'] = level

    heart_rate.to_csv(filename)

    letter_counts = Counter(level)
    heart_rate = pd.DataFrame.from_dict(letter_counts, orient='index')
    heart_rate.plot(kind='bar')

    plt.savefig("ranges_heart_rate.png")


def accelerometer_graphing(accelerometer, num):

    x = "accelerometer" + str(num) + "x"
    y = "accelerometer" + str(num) + "y"
    z = "accelerometer" + str(num) + "z"

    # prints 3 line graphs of the data to separate x, y, and z out
    plt.subplot(3, 1, 1)
    plt.plot(accelerometer["time"], accelerometer[x], '.-')
    plt.title('Accelerometer 1')
    plt.ylabel('X acceleration')

    plt.subplot(3, 1, 2)
    plt.plot(accelerometer["time"], accelerometer[y], '.-')
    plt.xlabel('time (s)')
    plt.ylabel('Y acceleration')
    plt.subplot(3, 1, 3)
    plt.plot(accelerometer["time"], accelerometer[y], '.-')
    plt.xlabel('time (s)')
    plt.ylabel('Z acceleration')

    plt.savefig("three_line_plot_accelerometer.png")

    # 3d plot
    ax = plt.axes(projection='3d')
    ax.plot3D(accelerometer[x], accelerometer[y], accelerometer[z], "green")
    plt.savefig("three_demension_plot_accelerometer.png")


def force_graph(force_gauge):

    plt.plot(force_gauge["time"], force_gauge["strain gauge"])
    plt.xlabel("Time")
    plt.ylabel("Force")
    plt.title("Force Gauge Data over Time")

    plt.savefig("force_plot.png")


# imports the heart rate data as a pandas data frame
filename = "Constant_Sample_data.csv"
data = pd.read_csv(filename, parse_dates=["time"])

heart_rate_graphing(data, filename)
force_graph(data)
accelerometer_graphing(data, 1)
