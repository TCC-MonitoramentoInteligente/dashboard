from time import sleep
import datetime

from flask import Flask, jsonify, Response
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import socket
import gevent
import requests

import cv2
import numpy as np
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)


BROKER_ADDRESS = '10.1.0.2'
BACKEND_ADDRESS = '10.1.0.7'
OBJECT_DETECTION_ADDRESS = '10.1.0.3'
OBJECT_DETECTION_PORT = 8030
PORT = 8070

sock = None
connected = False
camera_monitor = None

AVAILABLE_EVENTS = {
    'object-detection/#',
    'fainting-recognition/#',
}

AVAILABLE_CAMERAS = []

INCOMING_EVENTS = []
thread = Thread()


class UpdateThread(Thread):
    # Thread to update front-end content frequently.
    def __init__(self):
        super(UpdateThread, self).__init__()

    def update_front_content(self):
        while True:
            socketio.emit('event', INCOMING_EVENTS)
            sleep(1)
            socketio.emit('camera', AVAILABLE_CAMERAS)
            sleep(5)

    def run(self):
        self.update_front_content()


def include_message(msg, status):
    msg = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  " + msg
    message = {
        'content': str(msg),
        'status': status,
    }
    INCOMING_EVENTS.insert(0, message)


def include_camera(_id):
    AVAILABLE_CAMERAS.append({'id': _id})


def remove_camera(_id):
    AVAILABLE_CAMERAS.remove({'id': _id})


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    for _event in AVAILABLE_EVENTS:
        client.subscribe(_event)


def on_message_object(client, userdata, msg):
    message = msg.payload.decode()
    content = "Object Detection Service: " + message
    print(msg.topic, content)
    if 'error' in msg.topic:
        include_message(content, 'warning')
    else:
        include_message(content, 'info')
        if 'Camera' in message:
            if 'unregistered' in message:
                remove_camera(int(message.split(' ')[1]))
            elif 'registered' in message:
                include_camera(int(message.split(' ')[1]))
            socketio.emit('camera', AVAILABLE_CAMERAS)

    socketio.emit('event', INCOMING_EVENTS)


def on_message_fainting(client, userdata, msg):
    message = msg.payload.decode()
    content = "Fainting Service: " + message
    print(msg.topic, content)
    if 'error' in msg.topic:
        include_message(content, 'warning')
    else:
        include_message(content, 'info')
    socketio.emit('event', INCOMING_EVENTS)


@app.route("/")
def index():
    return jsonify(INCOMING_EVENTS, AVAILABLE_CAMERAS)


@app.route("/send-test-event")
def event():
    include_message("Test message", 'danger')
    socketio.emit('event', INCOMING_EVENTS)
    return jsonify('Event sent.')


# Reference: https://stackoverflow.com/questions/49939859/flask-video-stream-using-opencv-images
def video_debug_receiver():
    global sock
    global camera_monitor
    buffer_size = 65536
    while connected:
        data = b''
        sock.settimeout(5.0)
        try:
            data += sock.recv(buffer_size)
            a = data.find(b'\xff\xd8')
            b = data.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = data[a:b + 2]
                # data = data[b + 2 + 8:]
                image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                ret, jpeg = cv2.imencode('.jpg', image)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except socket.timeout:
            # If not available monitor, remove camera_monitor camera,
            camera_monitor = None
            yield (b'error')
            gevent.sleep(1)
            # image = cv2.imread('no-image.jpg', cv2.IMREAD_COLOR)
            # ret, jpeg = cv2.imencode('.jpg', image)
            # frame = jpeg.tobytes()
            # yield (b'--frame\r\n'
            #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        sock.settimeout(None)
        gevent.sleep()


@app.route("/monitor-video")
def video():
    return Response(video_debug_receiver(), mimetype='multipart/x-mixed-replace; boundary=frame')


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.message_callback_add('object-detection/logs/success', on_message_object)
    client.message_callback_add('object-detection/logs/error', on_message_object)
    client.message_callback_add('fainting-recognition/logs/success', on_message_fainting)
    client.message_callback_add('fainting-recognition/logs/error', on_message_fainting)
    client.connect(BROKER_ADDRESS)
    client.loop_start()


@socketio.on('connect')
def on_connect_socketio():
    global thread
    if not thread.isAlive():
        thread = UpdateThread()
        thread.start()


@socketio.on('enable_camera')
def send_monitor(cam_id):
    global sock
    global connected
    global camera_monitor

    # If request again, without timeout for the same camera don't request.
    if camera_monitor == cam_id:
        return
    if sock:
        sock.close()
    connected = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((BACKEND_ADDRESS, 0))
    sock.setblocking(False)
    port = sock.getsockname()[1]

    data = {
        'cam_id': int(cam_id),
        'client_ip': BACKEND_ADDRESS,
        'client_port': port,
    }
    print("enable monitor debug video", cam_id, port)
    requests.post(url='http://{}:{}/object-detection/monitor/'.format(OBJECT_DETECTION_ADDRESS, OBJECT_DETECTION_PORT), timeout=10, data=data)
    camera_monitor = cam_id


if __name__ == 'main':
    app.secret_key = 'super secret key'
    start_mqtt()
    socketio.run(app, host=BACKEND_ADDRESS, debug=True, port=PORT, use_reloader=False)
