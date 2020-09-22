# https://www.hackster.io/ruchir1674/video-streaming-on-flask-server-using-rpi-ef3d75

from flask import Flask, render_template, Response, redirect
import picamera
import cv2
import socket
import io

import car

app = Flask(__name__)
vc = cv2.VideoCapture(0)


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    # Video streaming generator function.
    while True:
        rval, frame = vc.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag.
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/motor/<direction>')
@app.route('/motor/<direction>/<speed>')
def move(direction, speed=35):
    car.move(direction, speed)
    return "done"


if __name__ == '__main__':
    car.setup()
    app.run(host='0.0.0.0', debug=False, threaded=True)
