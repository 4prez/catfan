# description
# RPi program to run a fan based on distance sensor trip or manual intervention
# Button: if not running - run as trigger, if running - stop running
# Sensor: based on depth, if not running trigger fan
# Blackout: time window where Sensor does not trip

# structure
# check if running on Pi
# load packages
# log boot
# initiate variables
# start loop
# check for triggers
# fan control
# loop






# load packages
#
import datetime as dt
import os
import sys
import time


# Check if running on Pi (linux) vs windows (for development)
On_Raspberry = not (sys.platform == 'win32') # determine if running on Windows or Pi (for inputs)
print("Running on Raspberry:",On_Raspberry)

if On_Raspberry == True:
    print("On Rasp")
    import RPi.GPIO as GPIO

path_abs = os.path.dirname(os.path.abspath(__file__))
print(path_abs)

# host_name = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
# print("Hostname :  ", host_name)
#print("IP : ", host_ip)
# print("")

# log startup-reboot
time_reboot = dt.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
startup_csv_path = str(os.path.join(path_abs, 'startup.csv'))
print(startup_csv_path)
with open(startup_csv_path, 'a') as fd:
    fd.write(time_reboot)
    fd.write("\n")

# initalize variables
Exit_Now = False
write_freq = 5  # in seconds
ctrl_freq = write_freq
time_last_write = dt.datetime.now()

# loop start
while not Exit_Now:
    print(dt.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
    time.sleep(1)

if On_Raspberry == True:
    GPIO.cleanup()
    lcd.lcd_clear()