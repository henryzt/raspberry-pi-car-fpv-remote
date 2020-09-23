import servo
import motor
import threading

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
                us_avoid()
            else:
                motor.t_up(50, 0)
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