class MqttSettings:
    def __init__(self):
        self.user = "pitero"
        self.key = "aio_qggT69JUOUp0ZNkZkGKyFHBDM8CR"
        self.port: int = 8883
        self.host = "io.adafruit.com"
        self.keepalive = 80
        self.commandTopic = "pitero/feeds/test1"
        self.telemetryTopic = "pitero/feeds/test2"
