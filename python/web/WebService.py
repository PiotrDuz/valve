import threading
import time

from flask import Flask, request

myApp = Flask(__name__)


def start():
    threading.Thread(myApp.run(host='0.0.0.0', port=46001)).start()


@myApp.route('/wifi', methods=['POST'])
def setWifi():
    data = request.get_json()
    print(data["password"])
    print(data["login"])
    return "OK"


@myApp.route('/adafruit', methods=['POST'])
def setAdafruit():
    data = request.get_json()
    print(data["password"])
    print(data["login"])
    return "OK"


@myApp.route('/calibrate', methods=['POST'])
def calibrate():
    data = request.get_json()
    time.sleep(5)
    return "OK"
