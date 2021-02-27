from datetime import datetime

import paho.mqtt.client as mqtt

from python.physical import SensorFactory
from python.position import ValveController, PositionCalculator
from python.storage import FileStorage


def getInstance():
    if MqttHandler._instance is None:
        MqttHandler._instance = MqttHandler()
    return MqttHandler._instance


class MqttHandler:
    _instance = None

    def __init__(self):
        self._settings = FileStorage.getInstance().getMqttSettings()
        self._valve = ValveController.getInstance()
        self._calc = PositionCalculator.getInstance()
        self._temp = SensorFactory.getInstance().getTempSensor()
        self._client = mqtt.Client()
        self._setupClient()

    def _setupClient(self):
        self._client.tls_set_context()
        self._client.username_pw_set(self._settings.user, self._settings.key)
        self._client.on_connect = self._mqtt_connect
        # self._client.on_disconnect = self._mqtt_disconnect
        self._client.on_message = self._mqtt_message
        # self._client.on_subscribe = self._mqtt_subscribe

    def startConnection(self):
        self._client.connect(self._settings.host, port=self._settings.port,
                             keepalive=self._settings.keepalive)
        self._client.loop_start()

    def stopConnection(self):
        self._client.loop_stop()

    def _mqtt_connect(self, client, userdata, flags, rc):
        self._client.subscribe(self._settings.commandTopic)
        self._client.subscribe(self._settings.telemetryTopic)
        print("Connect started. Result: " + str(rc))

    def _mqtt_message(self, client, userdata, msg):
        """Format: position;date """
        if msg.topic == self._settings.commandTopic:
            payload: str = msg.payload.decode('utf-8')
            wantedValvePosition = float(payload.split(";")[0])
            self._valve.setValvePosition(wantedValvePosition)
            print(wantedValvePosition)

    def publishTemperatureAndPosition(self):
        """ Format: temperature;position;currDate """
        temperature = self._temp.getTemp()
        position = self._calc.getPosition()
        currDate: str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        payloadValue = ";".join([str(temperature), str(position), str(currDate)])
        self._client.publish(self._settings.telemetryTopic, payload=payloadValue)
