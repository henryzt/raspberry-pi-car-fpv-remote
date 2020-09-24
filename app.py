# https://www.hackster.io/ruchir1674/video-streaming-on-flask-server-using-rpi-ef3d75

from flask import Flask, render_template, Response, redirect
from flask_socketio import SocketIO
import picamera
import cv2
import socket
import io

app = Flask(__name__)
socketio = SocketIO(app)
vc = cv2.VideoCapture(0)

import car

@app.route('/')
def index():
    return render_template('index.html')


def gen():
    # Video streaming generator function.
    while True:
        rval, frame = vc.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag.
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('connected')
def handle_connected(message):
    print("client connected", message)

@socketio.on('motor')
def move(json):
    car.move_motor(json['direction'], json['speed'])

@socketio.on('gimbal')
def gimbal(json):
    car.move_gimbal(json['direction'], json['speed'])

@socketio.on('autopilot')
def autopilot(json):
    car.toggle_autopilot()


if __name__ == '__main__':
    car.setup()
    socketio.run(app, host='0.0.0.0')
