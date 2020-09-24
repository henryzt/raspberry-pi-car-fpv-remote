import threading

import motor
import ranging
import servo
import autopilot

from connect import socket_emit

us_avoid = True
ir_avoid = False

# ------- motor -------


def move_motor(direction, speed=30):
    thread = threading.Thread(target=move_motor_thread, args=(direction, int(speed)))
    thread.start()


def move_motor_thread(direction, speed):
    print("Motor Signaled: " + direction, speed)
    if direction == "up":
        if not us_avoid or (us_avoid and range > 15):
            motor.t_up(speed, 6)
        else:
            report_obstacle(direction, range)
    elif direction == "left":
        if not ir_avoid or (ir_avoid and ranging.ir_left()):
            motor.t_left(speed, 1)
        else:
            report_obstacle(direction, range)
    elif direction == "right":
        if not ir_avoid or (ir_avoid and ranging.ir_right()):
            motor.t_right(speed, 1)
        else:
            report_obstacle(direction, range)
    elif direction == "down":
        motor.t_down(speed, 6)
    elif direction == "buzz":
        motor.buzz()
    elif direction == "brake":
        motor.t_stop(5)
        autopilot.stop()
    else:
        motor.t_stop(1)

# ------- gimbal -------

def move_gimbal(direction, speed=20):
    servo.move_gimbal(direction, int(speed) / 200)

# ------- ranging -------


def set_interval(func, sec):
    # ref https://stackoverflow.com/questions/2697039/
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.daemon = True
    t.start()
    return t


def get_us_range():
    global range, left, right
    range = ranging.us_distance()
    left = ranging.ir_left()
    right = ranging.ir_right()
    if ((motor.motor_status == "up" and us_avoid and range < 15) or
        (motor.motor_status == "left" and ir_avoid and not ranging.ir_left()) or
            (motor.motor_status == "right" and ir_avoid and not ranging.ir_right())):
        report_obstacle(motor.motor_status, range)
        motor.t_stop(1)
    # print("US - %s, Left - %s, Right - %s" % (range, left, right))
    return range


# ------- autopilot -------

def toggle_autopilot():
    if autopilot.autopilot:
        autopilot.stop()
    else:
        autopilot.start()

def report_obstacle(direction, range):
    socket_emit("obstacle", {"direction": direction, "range": range })
    motor.buzz()

# ------- setup -------

def setup():
    motor.setup()
    ranging.setup()
    servo.reset_all()
    set_interval(get_us_range, 0.1)
