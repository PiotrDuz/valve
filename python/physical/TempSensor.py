from adafruit_ads1x15 import ads1015
from adafruit_ads1x15.analog_in import AnalogIn


class TempSensor:

    def __init__(self, chan: AnalogIn, ads: ads1015):
        self._channel = chan
        self._ads = ads

    def getTemp(self):
        rawValueMiliV = self._channel.voltage * 1000 # voltages not affected by gain
        temp = (rawValueMiliV - 500) / 10.0
        return temp
