import sys
import time

from python.fileHandling import RestartService
from python.physical import Button, Leds
from python.web import AccessPoint, WebService
from python.web.mqtt import MqttHandler


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
        else:
            leds.setRedOff()
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

    status = startConnection()
    if status:
        handleNormalOperation()
    handleConfigurationMode()

