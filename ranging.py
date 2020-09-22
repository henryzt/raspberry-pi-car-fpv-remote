import RPi.GPIO as GPIO
import time
import sys

TRIG = 20
ECHO = 21

SensorRight = 16
SensorLeft  = 12


def setup():
    # Ultrasonic ranging
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    # Infrared
    GPIO.setup(SensorRight,GPIO.IN)
    GPIO.setup(SensorLeft,GPIO.IN)


def us_distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100


def us_loop():
    while True:
        dis = distance()
        if (dis < 40) == True:
            while (dis < 40) == True:
                t_down(50, 0.5)
                t_right(50, 0.1)
                dis = distance()
        else:
            t_up(50, 0)
        print(dis, 'cm')
        print('')


def ir_left():
    return GPIO.input(SensorLeft)

def ir_right():
    return GPIO.input(SensorRight)