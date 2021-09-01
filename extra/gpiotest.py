import RPi.GPIO as GPIO
import time

def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)

def set_gpio_0():
    GPIO.output(21, 0)
    
def set_gpio_1():
    GPIO.output(21, 1)

while(1):
    inp = input("enter: ")

    if(inp=='1'):
        print("set up")
        gpio_setup()
    elif(inp=='2'):
        print("gpio 0")
        set_gpio_0()
    elif(inp=='3'):
        print("gpio 1")
        set_gpio_1
    elif(inp=='4'):
        break