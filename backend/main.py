from flask import Flask, jsonify, Response
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import socket
import gevent

import cv2
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)
port = 8070


BROKER_ADDRESS = '10.1.0.2'
MONITOR_ADDRESS = '10.1.0.7'  # IP from machine running this code.
MONITOR_PORT_ADDRESS = 5005


sock = None
connected = False
data = None

AVAILABLE_EVENTS = {
    'object-detection/#',
    'fainting-recognition/#',
}

INCOMING_EVENTS = []


def include_message(msg, status):
    message = {
        'content': str(msg),
        'status': status,
    }
    INCOMING_EVENTS.append(message)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    for _event in AVAILABLE_EVENTS:
        client.subscribe(_event)


def on_message_object(client, userdata, msg):
    message = msg.payload.decode()
    print("Object: ", msg.topic, message)
    if 'error' in msg.topic:
        include_message("Object: " + message, 'warning')
    else:
        include_message("Object: " + message, 'info')
    socketio.emit('event', INCOMING_EVENTS)


def on_message_fainting(client, userdata, msg):
    message = msg.payload.decode()
    print("Fainting: ", msg.topic, message)
    if 'error' in msg.topic:
        include_message("Object: " + message, 'warning')
    else:
        include_message("Fainting: " + message, 'info')
    socketio.emit('event', INCOMING_EVENTS)


@app.route("/")
def index():
    return jsonify(INCOMING_EVENTS)


@app.route("/send-test-event")
def event():
    include_message("Test message", 'danger')
    socketio.emit('event', INCOMING_EVENTS)
    return jsonify('Event sent.')


# Reference: https://stackoverflow.com/questions/49939859/flask-video-stream-using-opencv-images
def video_debug_receiver():
    global sock
    global data
    buffer_size = 65536
    while connected:
        data += sock.recv(buffer_size)
        a = data.find(b'\xff\xd8')
        b = data.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = data[a:b + 2]
            data = data[b + 2 + 8:]
            image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
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


def start_sock():
    global data
    global connected
    global sock

    if not connected:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((MONITOR_ADDRESS, MONITOR_PORT_ADDRESS))
        data = b''
        connected = True


if __name__ == 'main':
    app.secret_key = 'super secret key'
    start_mqtt()
    start_sock()
    socketio.run(app, host=MONITOR_ADDRESS, debug=True, port=port, use_reloader=False)
