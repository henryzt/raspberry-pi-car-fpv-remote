import servo
import motor
import ranging
import threading

from connect import socket_emit

autopilot = None


class AutopilotTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while self._running:
            dis1 = servo.front_detection()
            if (dis1 < 40) == True:
                socket_emit("obstacle", {"direction": "up", "range": dis1 })
                us_avoid()
            else:
                ir_avoid()
        print("autopilot terminated")


def us_avoid():
    motor.t_stop(0.2)
    motor.t_down(50, 0.5)
    motor.t_stop(0.2)
    dis2 = servo.left_detection()
    dis3 = servo.right_detection()
    if (dis2 < 40) == True and (dis3 < 40) == True:
        motor.t_left(50, 1)
    elif (dis2 > dis3) == True:
        motor.t_left(50, 0.3)
        motor.t_stop(0.1)
    else:
        motor.t_right(50, 0.3)
        motor.t_stop(0.1)


def ir_avoid():
    print("ir avoiding")
    SR_2 = ranging.ir_right()
    SL_2 = ranging.ir_left()
    if SL_2 == True and SR_2 == True:
        motor.t_up(50, 0)
    elif SL_2 == True and SR_2 == False:
        motor.t_left(50, 0)
    elif SL_2 == False and SR_2 == True:
        motor.t_right(50, 0)
    else:
        motor.t_stop(0.3)
        motor.t_down(50, 0.4)
        motor.t_left(50, 0.5)


def start():
    global autopilot
    stop()
    autopilot = AutopilotTask()
    t = threading.Thread(target=autopilot.run)
    t.start()


def stop():
    global autopilot
    if autopilot:
        autopilot.terminate()
        autopilot = None
        servo.center_us()
