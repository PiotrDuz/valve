class MqttSettings:
    def __init__(self):
        self.user = "pitero"
        self.key = "aio_syBD70Bj7lsUJdaodABENIV6D06a"
        self.port = "8883"
        self.host = "io.adafruit.com"
        self.keepalive = 80
        self.commandTopic = "pitero/feeds/command"
        self.telemetryTopic = "pitero/feeds/telemetry"
        self.secured = "yes"
