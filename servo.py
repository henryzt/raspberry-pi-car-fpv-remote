from adafruit_servokit import ServoKit
import time
import threading

kit = ServoKit(channels=16)

servo_us = kit.servo[0]
servo_cam_y = kit.servo[1]
servo_cam_x = kit.servo[2]

cam_y_deg = 0
cam_x_deg = 90


# ------- ultrasonic -------

def center_us():
    servo_us.angle = 90

# ------- gimbal -------


def reset_cam():
    global cam_x_deg, cam_y_deg
    cam_y_deg = 0
    cam_x_deg = 90
    servo_cam_y.angle = 0
    servo_cam_x.angle = 90


def move_cam_x(direction, speed):
    global cam_x_deg
    delta = speed if direction == "right" else -speed
    new_deg = cam_x_deg + delta / 30
    if 0 <= new_deg <= 180:
        cam_x_deg = new_deg
        servo_cam_x.angle = cam_x_deg
        return True
    return False


def move_cam_y(direction, speed):
    global cam_y_deg
    delta = speed if direction == "up" else -speed
    new_deg = cam_y_deg + delta / 30
    if 0 <= new_deg <= 180:
        cam_y_deg = new_deg
        servo_cam_y.angle = cam_y_deg
        return True
    return False


class MoveGimbalServo:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, direction, speed):
        movable = True
        while self._running and movable:
            movable = move_gimbal_thread(direction, speed)
        print("terminated")


def move_gimbal_thread(direction, speed):
    if direction == "left" or direction == "right":
        return move_cam_x(direction, speed)
    elif direction == "up" or direction == "down":
        return move_cam_y(direction, speed)
    else:
        return False


gimbal_task = None

def move_gimbal(direction, speed):
    global gimbal_task
    if gimbal_task:
        gimbal_task.terminate()
    gimbal_task = MoveGimbalServo()
    t = threading.Thread(
        target=gimbal_task.run, args=(direction, speed))
    t.start()

# ------- common -------


def reset_all():
    center_us()
    reset_cam()
