#!/usr/bin/python

import time
import RPi.GPIO as GPIO

PWMA   = 18
AIN1   = 22
AIN2   = 27

PWMB   = 23
BIN1   = 25
BIN2   = 24

BtnPin  = 19
Gpin    = 5
Rpin    = 6

buzzer = 17

blocking = 0

def t_up(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)
        
def t_stop(t_time):
        L_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def t_down(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def t_left(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_right(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def buzz():
        Buzz = GPIO.PWM(buzzer, 440)
        Buzz.start(50)
        Buzz.ChangeFrequency(2000)
        time.sleep(0.5)
        Buzz.stop()

def keysacn():
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)
        else:
            GPIO.output(Rpin,0)
            
def setup():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(AIN2,GPIO.OUT)
        GPIO.setup(AIN1,GPIO.OUT)
        GPIO.setup(PWMA,GPIO.OUT)

        GPIO.setup(BIN1,GPIO.OUT)
        GPIO.setup(BIN2,GPIO.OUT)
        GPIO.setup(PWMB,GPIO.OUT)
        GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
        GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(buzzer, GPIO.OUT)    # buzzer

        
def destroy():
	GPIO.cleanup()	

if __name__ == '__main__':
        setup()
        L_Motor= GPIO.PWM(PWMA,100)
        L_Motor.start(0)
        R_Motor = GPIO.PWM(PWMB,100)
        R_Motor.start(0)
        print("motor ready.")
        buzz()
        keysacn()
        try:
                t_up(30,2)
        except KeyboardInterrupt:
                GPIO.cleanup()


    

