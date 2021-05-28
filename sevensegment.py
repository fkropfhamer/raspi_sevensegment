#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
#    1_____
#    2/  /3
#   4-----
#   5/   /6
#    7-----  . 8
_numbers = [2,3,4,17]  # number on/off connection 1-4

_segment = [21,20,14,15,16,18,27,22]  # segments connection 1-8

translation = {
    "0": (1, 1, 1, 0, 1, 1, 1, 0),
    "1": (0, 0, 1, 0, 0, 1, 0, 0),
    "2": (1, 0, 1, 1, 1, 0, 1, 0),
    "3": (1, 0, 1, 1, 0, 1, 1, 0),
    "4": (0, 1, 1, 1, 0, 1, 0, 0),
    "5": (1, 1, 0, 1, 0, 1, 1, 0),
    "6": (1, 1, 0, 1, 1, 1, 1, 0),
    "7": (1, 0, 1, 0, 0, 1, 0, 0),
    "8": (1, 1, 1, 1, 1, 1, 1, 0),
    "9": (1, 1, 1, 1, 0, 1, 1, 0),
    "*": (1, 1, 1, 1, 0, 0, 0, 0),
    "C": (1, 1, 0, 0, 1, 0, 1, 0) 
}

_segment0 = [1, 0, 0, 0, 0, 0, 0, 0]
_segment1 = [0, 1, 0, 0, 0, 0, 0, 0]
_segment2 = [0, 0, 1, 0, 0, 0, 0, 0]
_segment3 = [0, 0, 0, 1, 0, 0, 0, 0]
_segment4 = [0, 0, 0, 0, 1, 0, 0, 0]
_segment5 = [0, 0, 0, 0, 0, 1, 0, 0]
_segment6 = [0, 0, 0, 0, 0, 0, 1, 0]
_segment7 = [0, 0, 0, 0, 0, 0, 0, 1]

for i in _segment:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)
for k in _numbers:
    GPIO.setup(k, GPIO.OUT)
    GPIO.output(k, GPIO.LOW)


def display(display0, display1, display2, display3):
    def segment_display(display):
            for i in range(0,8):
                if display[i] == 1:
                    GPIO.output(_segment[i], GPIO.HIGH)
                else:
                    GPIO.output(_segment[i], GPIO.LOW)
                #time.sleep(0.0001)

    for i in range(4):
        time.sleep(0.0001)
        if i == 0:
            segment_display(display0)
        elif i == 1:
            segment_display(display1)
        elif i == 2:
            segment_display(display2)
        else:
            segment_display(display3)
        GPIO.output(_numbers[i], GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(_numbers[i], GPIO.HIGH)
        
        #reset()
        
        #GPIO.output(i, GPIO.HIGH)

        

def reset():
    for i in _numbers:
        GPIO.output(i, GPIO.HIGH)
    for j in _segment:
        GPIO.output(j, GPIO.LOW)

def point(tdisplay):
    temp = list(tdisplay)
    temp[7]= 1
    return temp

def strtime():
    t = time.strftime("%H%M")
    return t

def coretemp():
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    cputemp = tempFile.read()
    tempFile.close()
    return str(round(float(cputemp) / 1000))

_intervall = 1000

def main():
    try:
        while True:
            current_time = strtime()        #time.sleep(0.2)
            for _ in range(0, _intervall):
                display(translation[current_time[0]], point(translation[current_time[1]]), translation[current_time[2]], translation[current_time[3]])
            temperature = coretemp()
            for _ in range(0, _intervall):
                display(translation[temperature[0]], translation[temperature[1]], translation["*"], translation["C"])    
    except:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
