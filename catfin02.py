# DESCRIPTION
# RPi program to run a fan based on distance sensor trip or manual intervention
# Button: if not running - run as trigger, if running - stop running
# Sensor: based on depth, if not running trigger fan
# Blackout: time window where Sensor does not trip

# STRUCTURE
# load general packages
# check if running on Pi
# load Pi packages / GPIO setup
# log boot
# initiate variables
# start loop
# check for triggers
# fan control
# loop






# LOAD PACKAGES
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
    # Setup Distance Sensor
    GPIO.setmode(GPIO.BOARD)
    PIN_TRIGGER = 7
    PIN_ECHO = 11
    PIN_FAN = 37
    GPIO.setup(PIN_ECHO, GPIO.IN)
    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    GPIO.setup(PIN_FAN, GPIO.OUT)
    GPIO.output(PIN_FAN, GPIO.HIGH)

    print("Waiting for sensor to settle")
    time.sleep(2)



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
distance_trigger = 12 # in
distance_exit = 6 # in
fan_duration = 10 # in seconds
black_out_start_01 = dt.time(3, 25, 56)
black_out_duration_01 = 15 # minutes
# black_out_end_01 = black_out_start_01 + black_out_duration_01*60
black_out_start_02 = dt.time(15, 25, 0)
black_out_duration_02 = 15 # minutes
# black_out_end_02 = black_out_start_02 + timedelta(minutes=black_out_duration_02)

Exit_Now = False
fan_run = False
fan_trigger_distance = True
fan_trigger_button = False

fan_end_time = dt.datetime.now() + dt.timedelta(seconds=fan_duration)

# LOOP START
while not Exit_Now:
    print(dt.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

    # CHECK FOR TRIGGERS

    # BUTTON TRIGGER

    # DISTANCE TRIGGER
    if On_Raspberry == True:
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        current_distance = round(pulse_duration * 6752, 1)
        print("Distance:", current_distance, "in")
        # ignore if during blackout
        black_out = False
        if black_out == False and current_distance < distance_trigger:
            fan_trigger_distance = True
        if current_distance < distance_exit:
                Exit_Now = True



    # FAN CONTROL
    if fan_run == True and dt.datetime.now() > fan_end_time:
        fan_run = False
    if fan_trigger_distance == True:
        fan_run = True
        fan_end_time = dt.datetime.now() + dt.timedelta(seconds=fan_duration)
        fan_trigger_distance = False
    if fan_trigger_button == True and fan_run == True:
        fan_run = not(False)
        fan_trigger_button = False

    if fan_run == True:
        print("True: " + str(fan_run))
        if On_Raspberry == True:
            GPIO.output(PIN_FAN, GPIO.HIGH)

    if fan_run == False:
        print("False: " + str(fan_run))
        if On_Raspberry == True:
            GPIO.output(PIN_FAN, GPIO.LOW)

    # prepare for loop
    time.sleep(1)

if On_Raspberry == True:
    GPIO.cleanup()



