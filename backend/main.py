from flask import Flask, render_template, request, jsonify, redirect
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


def on_connect(client, rc):
    print("Connected with result code " + str(rc))

    for _event in AVAILABLE_EVENTS:
        client.subscribe(_event)


def on_message_object(msg):
    print("Object: ", msg.topic, str(msg.payload))
    include_message(str(msg.payload), 'info')
    socketio.emit('event', INCOMING_EVENTS)


def on_message_fainting(msg):
    print("Fainting: ", msg.topic, str(msg.payload))
    include_message(str(msg.payload), 'info')
    socketio.emit('event', INCOMING_EVENTS)


@app.route("/")
def index():
    return jsonify(INCOMING_EVENTS)
    # return render_template('dashboard.html')


@app.route("/send-event")
def event():
    include_message("Mensagem qualquer", 'danger')
    socketio.emit('event', INCOMING_EVENTS)
    return jsonify('Evento enviado')


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.message_callback_add('object-detection/objects', on_message_object)
    client.message_callback_add('object-detection/logs/success', on_message_object)
    client.message_callback_add('object-detection/add', on_message_object)
    client.message_callback_add('object-detection/remove', on_message_object)
    client.message_callback_add('object-detection/add', on_message_object)
    client.message_callback_add('fainting-recognition/logs/success', on_message_fainting)
    client.message_callback_add('fainting-recognition/logs/error', on_message_fainting)

    client.connect(broker_address)
    client.loop_start()


if __name__ == 'main':
    app.secret_key = 'super secret key'

    start_mqtt()
    # app.run()
    socketio.run(app, debug=True)
