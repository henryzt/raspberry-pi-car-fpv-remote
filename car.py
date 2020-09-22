import motor 
import threading

def move(direction, speed):
    thread = threading.Thread(target=move_motor, args=(direction, int(speed)))
    thread.start()

def move_motor(direction, speed):
    print("Motor Signaled: " + direction)
    if direction == "forward":
        motor.t_up(speed, 6)
    elif direction == "backward":
        motor.t_down(speed, 6)
    elif direction == "left":
        motor.t_left(40, 1)
    elif direction == "right":
        motor.t_right(40, 1)
    elif direction == "buzz":
        motor.buzz()
    else:
        motor.t_stop(1)

def setup():
    motor.setup_gpio()
