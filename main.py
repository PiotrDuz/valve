import sys
import time

from python.fileHandling import RestartService
from python.physical import Button, Leds, MotorController, SensorFactory
from python.position import ValveController
from python.web import AccessPoint, WebService
from python.web.mqtt import MqttHandler

import board
import busio
from adafruit_ads1x15 import ads1015
from adafruit_ads1x15.analog_in import AnalogIn

def wait():
    time.sleep(0.5)


def startConnection() -> bool:
    successful = True
    try:
        mqtt.startConnection()
    except:
        successful = False
    return successful


def handleNormalOperation():
    print("Normal operation")
    leds.setGreenOff()
    leds.setRedOff()
    while button.isNotPressed():
        if not mqtt.isConnected():
            leds.setRedOn()
        mqtt.publishTemperatureAndPosition()
        wait()


def handleConfigurationMode():
    print("Configuration mode")
    leds.setGreenOn()
    leds.setRedOff()
    mqtt.stopConnection()
    ap.switchToAccessPoint()
    server.start()
    while button.isNotPressed():
        wait()
    leds.setRedOn()
    leds.setGreenOn()
    restartService.restart()

if __name__ == '__main__':
    server = WebService
    button = Button.getInstance()
    leds = Leds.getInstance()
    mqtt = MqttHandler.getInstance()
    ap = AccessPoint.getInstance()
    restartService = RestartService.getInstance()

    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ads1015.ADS1015(i2c, data_rate=2400, gain=1)
    chan1 = AnalogIn(ads, ads1015.P2)
    chan2 = AnalogIn(ads, ads1015.P3)
    for i in range(240):
        print('chan1: '+str(chan1.value) + ' v1: ' + str(chan1.voltage) + ' chan2: ' + str(chan2.value) + ' v2:' + str(chan2.voltage))
        wait()

    # status = startConnection()
    # if status:
    #     handleNormalOperation()
    # handleConfigurationMode()

