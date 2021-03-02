import time
from datetime import datetime

import paho.mqtt.client as mqtt

from python.fileHandling.storage import FileStorage


def getInstance():
    if MqttHandler._instance is None:
        MqttHandler._instance = MqttHandler()
    return MqttHandler._instance


class MqttHandler:
    _instance = None

    def __init__(self):
        self._settings = FileStorage.getInstance().getMqttSettings()
        # self._valve = ValveController.getInstance()
        # self._calc = PositionCalculator.getInstance()
        # self._temp = SensorFactory.getInstance().getTempSensor()
        self._client = mqtt.Client()
        self._isCommandRunning = False
        self._timer = time.time()
        self._setupClient()

    def _setupClient(self):
        self._client.tls_set_context()
        self._client.username_pw_set(self._settings.user, self._settings.key)
        self._client.on_connect = self._mqttConnect
        self._client.on_disconnect = self._mqttDisconnect
        self._client.on_message = self._mqttMessage
        # self._client.on_subscribe = self._mqtt_subscribe

    def startConnection(self):
        self._client.connect(self._settings.host, port=self._settings.port,
                             keepalive=self._settings.keepalive)
        self._client.loop_start()

    def stopConnection(self):
        self._client.loop_stop()

    def _mqttDisconnect(self, client, userdata, rc):
        print("Disconnected")

    def _mqttConnect(self, client, userdata, flags, rc):
        self._client.subscribe(self._settings.commandTopic)
        self._client.subscribe(self._settings.telemetryTopic)
        print("Connect started. Result: " + str(rc))

    def _mqttMessage(self, client, userdata, msg):
        """Format: position;date """
        if msg.topic == self._settings.commandTopic:
            self._isCommandRunning = True
            payload: str = msg.payload.decode('utf-8')
            wantedValvePosition = float(payload.split(";")[0])
            # self._valve.setValvePosition(wantedValvePosition)
            print(wantedValvePosition)
            self._resetTimer()
            self._publishTemperatureAndPositionWithoutValidation()
            self._isCommandRunning = False

    def publishTemperatureAndPosition(self):
        """ Format: temperature;position;currDate """
        if self._hasEnoughTimePassed() and self._client.is_connected() and not self._isCommandRunning:
            print("what")
            self._publishTemperatureAndPositionWithoutValidation()

    def _publishTemperatureAndPositionWithoutValidation(self):
        temperature = 34  # self._temp.getTemp()
        position = 2  # self._calc.getPosition()
        currDate: str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        payloadValue = ";".join([str(temperature), str(position), str(currDate)])
        self._client.publish(self._settings.telemetryTopic, payload=payloadValue)
        print("published")

    def _resetTimer(self):
        self._timer = time.time()

    def _hasEnoughTimePassed(self):
        hasPassed = time.time() - self._timer > 30
        print(str(time.time()) + str(hasPassed))
        if hasPassed:
            self._resetTimer()
        return hasPassed
