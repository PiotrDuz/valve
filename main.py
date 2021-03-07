import sys
import time

from python.fileHandling import RestartService
from python.physical import Button, Leds
from python.web import AccessPoint, WebService
from python.web.mqtt import MqttHandler


def waitAndFlushOutputs():
    time.sleep(0.5)
    sys.stdout.flush()
    sys.stderr.flush()


if __name__ == '__main__':
    server = WebService
    button = Button.getInstance()
    leds = Leds.getInstance()
    mqtt = MqttHandler.getInstance()
    ap = AccessPoint.getInstance()
    restartService = RestartService.getInstance()

    mqtt.startConnection()
    while True:
        if button.isPressed():
            leds.setGreenOff()
            leds.setRedOff()
            if not mqtt.isConnected():
                leds.setRedOn()
            mqtt.publishTemperatureAndPosition()
        else:
            break
        waitAndFlushOutputs()

    leds.setGreenOn()
    leds.setRedOff()
    mqtt.stopConnection()
    ap.switchToAccessPoint()
    server.start()

    while True:
        if button.isPressed():
            restartService.restart()
        waitAndFlushOutputs()

