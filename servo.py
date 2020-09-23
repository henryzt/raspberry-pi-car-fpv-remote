from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

servo_us = kit.servo[0]
servo_cam_y = kit.servo[1]
servo_cam_x = kit.servo[2]

servo_us.angle = 0
time.sleep(3)
servo_us.angle = 180
servo_cam_y.angle = 5
time.sleep(3)
servo_us.angle = 90
servo_cam_y.angle = 30
servo_cam_x.angle = 180
time.sleep(3)
servo_cam_y.angle = 0
servo_cam_x.angle = 90