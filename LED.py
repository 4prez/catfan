import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
FAN_PIN = 25
GPIO.setup(FAN_PIN,GPIO.OUT)
print("LED on")
GPIO.output(FAN_PIN,GPIO.HIGH)
time.sleep(1)
print("LED off")
GPIO.output(FAN_PIN,GPIO.LOW)
GPIO.cleanup()