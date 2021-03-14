from adafruit_ads1x15.analog_in import AnalogIn


class TempSensor:

    def __init__(self, chan: AnalogIn):
        self._channel = chan

    def getTemp(self):
        rawValueMiliV = self._channel.voltage * 1000  # voltages not affected by gain
        temp = (rawValueMiliV - 500) / 10.0
        return temp
