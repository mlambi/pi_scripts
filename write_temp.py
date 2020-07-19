#!/usr/bin/python3

# import libraries
# from envirophat we are only importing weather.
# light, weather, motion, analog, leds
# imporing datetime to get the timestamp

from envirophat import weather
from datetime import datetime

# temp will call the function to retreive temp data
# it comes as a long float reprecenting degress C
# commenting this out to try and define a function instead
# temp = weather.temperature()

# the time object gets raw data
# the strftime formats it
timeObj = datetime.now()
timestamp = timeObj.strftime("%H:%M:%S")

# define the file we will write to.
# Note: this is relative to where the script is run!
filename = "temp.txt"


def temp_in_F():
    reading = weather.temperature()
    ftemp = (reading  * 9/5) + 32
    F = str(int(ftemp))
    C = str(int(reading))
    return C, F

C, F = temp_in_F()

target = open(filename, 'w')
target.write(timestamp)
target.write("\n")
target.write(f"Temp in C: {C}")
target.write("\n")
target.write(f"Temp in F: {F}")
target.write("\n")

target.close()

