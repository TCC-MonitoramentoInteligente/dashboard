from flask import Flask, render_template, request, jsonify
from flask import request
from flask_socketio import SocketIO, send, emit
import paho.mqtt.client as mqtt
import json
import time


app = Flask(__name__)
socketio = SocketIO(app)

# broker_address = '10.1.0.4'
broker_address = 'localhost'
port = 5000


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe('object-detection/#')
    client.subscribe('fainting-recognition/#')
    client.subscribe('fake-data/#')


def on_message_object(client, userdata, msg):
    result = json.loads(msg.payload.decode())
    print("Object: ", result)


def on_message_fainting(client, userdata, msg):
    # result = json.loads(msg.payload.decode())
    print("Fainting: ", msg.payload.decode())


@app.route("/")
def index():
    return render_template('dashboard.html')


@app.route('/background_process')
def background_process():
    try:
        lang = request.args.get('proglang', 0, type=str)
        if lang.lower() == 'python':
            return jsonify(result='You are wise')
        else:
            return jsonify(result='Try again.')
    except Exception as e:
        return str(e)


@socketio.on('my event')
def handle_message(message):
    print('received message: ', message)
    time.sleep(10)
    for i in range(10):
        handle_my_custom_event()


@socketio.on('custom')
def handle_my_custom_event():
    emit('new message', 'msg teste')


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.message_callback_add('object-detection/objects', on_message_object)
    client.message_callback_add('fainting-recognition/logs/success', on_message_fainting)

    client.connect(broker_address)
    client.loop_start()


if __name__ == 'main':
    app.secret_key = 'super secret key'

    start_mqtt()
    # app.run()
    socketio.run(app, debug=True)
