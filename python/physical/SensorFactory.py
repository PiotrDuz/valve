import board
import busio
from adafruit_ads1x15 import ads1015
from adafruit_ads1x15.analog_in import AnalogIn

from python.physical.HallSensor import HallSensor
from python.physical.TempSensor import TempSensor


def getInstance():
    if HallSensorFactory._instance is None:
        HallSensorFactory._instance = HallSensorFactory()
    return HallSensorFactory._instance


class HallSensorFactory:
    _instance = None

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ads1015.ADS1015(i2c, data_rate=2400, gain=2)
        self.hallSensor = None
        self.tempSensor = None

    def getHallSensor(self) -> HallSensor:
        if self.hallSensor is None:
            chan = AnalogIn(self.ads, ads1015.P2, ads1015.P3)
            self.hallSensor = HallSensor(chan)
        return self.hallSensor

    def getTempSensor(self) -> TempSensor:
        if self.tempSensor is None:
            chan = AnalogIn(self.ads, ads1015.P0, ads1015.P1)
            self.tempSensor = TempSensor(chan)
        return self.tempSensor
