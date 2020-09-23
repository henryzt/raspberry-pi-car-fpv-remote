import threading

import motor
import ranging

us_avoid = True
ir_avoid = False

# ------- motor -------


def move(direction, speed):
    thread = threading.Thread(target=move_motor, args=(direction, int(speed)))
    thread.start()


def move_motor(direction, speed):
    print("Motor Signaled: " + direction)
    if direction == "up":
        if not us_avoid or (us_avoid and range > 15):
            motor.t_up(speed, 6)
        else:
            motor.buzz()
    elif direction == "left":
        if not ir_avoid or (ir_avoid and ranging.ir_left()):
            motor.t_left(speed, 1)
        else:
            motor.buzz()
    elif direction == "right":
        if not ir_avoid or (ir_avoid and ranging.ir_right()):
            motor.t_right(speed, 1)
        else:
            motor.buzz()
    elif direction == "down":
        motor.t_down(speed, 6)
    elif direction == "buzz":
        motor.buzz()
    else:
        motor.t_stop(1)

# ------- ranging -------


def set_interval(func, sec):
    # ref https://stackoverflow.com/questions/2697039/
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
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
        motor.t_stop(1)
        motor.buzz()
    # print("US - %s, Left - %s, Right - %s" % (range, left, right))
    return range


# ------- setup -------

def setup():
    motor.setup()
    ranging.setup()
    set_interval(get_us_range, 0.1)
