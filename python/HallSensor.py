from adafruit_ads1x15 import ads1015
from adafruit_ads1x15.analog_in import AnalogIn


class HallSensor:
    def __init__(self, channel: AnalogIn, ads: ads1015):
        self.channel = channel
        self.ads = ads

    def getValue(self):
        self.ads.gain = 2
        value = self.channel.value
        self.ads.gain = 1
        return value

    def getAveragedValue(self, avgPeriod):
        self.ads.gain = 2
        valueSum = 0
        for x in range(0, avgPeriod):
            valueSum = valueSum + self.channel.value
        self.ads.gain = 1
        return valueSum / avgPeriod
