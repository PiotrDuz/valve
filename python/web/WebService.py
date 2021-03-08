import threading
import time

from flask import Flask, request

from python.fileHandling import WifiConfigurator
from python.fileHandling.storage import FileStorage
from python.position import PositionCalibrator

myApp = Flask(__name__)


def start():
    threading.Thread(target=_runServer).start()

def _runServer():
    myApp.run(host='0.0.0.0', port=46001)

@myApp.route('/wifi', methods=['POST'])
def setWifi():
    data = request.get_json()
    wifi = WifiConfigurator.getInstance()
    wifi.setWifi(data["ssid"], data["password"])
    return "OK"


@myApp.route('/adafruit', methods=['POST'])
def setAdafruit():
    data = request.get_json()
    storage = FileStorage.getInstance()
    storage.setMqttCred(data["login"], data["key"])
    return "OK"


@myApp.route('/calibrate', methods=['POST'])
def calibrate():
    calibrator = PositionCalibrator.getInstance()
    calibrator.calibrate()
    return "OK"
