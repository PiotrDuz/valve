from adafruit_ads1x15.analog_in import AnalogIn


class HallSensor:

    def __init__(self, channel: AnalogIn):
        self.channel = channel

    def getValue(self):
        value = self.channel.value
        return value

    def getAveragedValue(self, avgPeriod):
        valueSum = 0
        for x in range(0, avgPeriod):
            valueSum = valueSum + self.channel.value
        return valueSum / avgPeriod
