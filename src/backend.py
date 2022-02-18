import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import time
import RPi.GPIO as GPIO
import logging

app = Flask(__name__)
CORS(app)
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(18, GPIO.IN, GPIO.PUD_UP)
SENSOR_MASA = 18
SENSOR_BOLETO = 22
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #* SENSOR DE MASA
GPIO.setup(SENSOR_BOLETO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # * SENSOR BOLETO
# global boleto 


estatus = 0
@app.before_request
def require_authorization():
    # CORS
    if request.method == 'OPTIONS':
        response = Response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Methods', 'DELETE,PUT,GET,POST')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        return response

@app.route("/", methods=['GET', 'POST'])
def Status():
    
    boleto = False
    sensor  = False
    if GPIO.input(SENSOR_BOLETO) == GPIO.LOW:
        boleto =  True
    if GPIO.input(SENSOR_MASA) == GPIO.HIGH:
        sensor = True
    response = {
        'boleto':boleto,
        'sensor':sensor
        }
    return jsonify(response)

@app.route("/open", methods=['GET', 'POST'])
def Open():
    GPIO.output(16, True)
    time.sleep(.2) 
    GPIO.output(16, False)
    time.sleep(.2)
    GPIO.output(16, True)
    time.sleep(.2)
    GPIO.output(16, False)
    time.sleep(.2)
    GPIO.output(16, True)
    time.sleep(.2)
    GPIO.output(16, False)
    return "ok"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
