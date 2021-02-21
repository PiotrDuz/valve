from adafruit_ads1x15.analog_in import AnalogIn


class TempSensor:
    def __init__(self, chan: AnalogIn):
        self.channel = chan

    def getValue(self):
        return self.channel.value
