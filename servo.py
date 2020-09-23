from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

servo_us = kit.servo[0]
servo_cam_y = kit.servo[1]
servo_cam_x = kit.servo[2]

cam_y_deg = 0
cam_x_deg = 90


def center_us():
  servo_us.angle = 90

def reset_cam():
  global cam_x_deg, cam_y_deg
  cam_y_deg = 0
  cam_x_deg = 90
  servo_cam_y.angle = 0
  servo_cam_x.angle = 90

def move_cam_x(direction, speed):
  global cam_x_deg
  delta = speed if direction == "right" else -speed
  new_deg = cam_x_deg + delta
  if 0 <= new_deg <= 180:
    cam_x_deg = new_deg
    servo_cam_x.angle = cam_x_deg


def reset_all():
  center_us()
  reset_cam()

def test():
  servo_us.angle = 0
  time.sleep(3)
  servo_us.angle = 180
  servo_cam_y.angle = 5
  time.sleep(3)
  servo_us.angle = 90
  servo_cam_y.angle = 30
  servo_cam_x.angle = 180
  time.sleep(3)
  