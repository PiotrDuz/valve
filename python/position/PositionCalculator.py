from python.physical import SensorFactory
from python.position.ValveOpenLookup import ValveOpenLookup
from python.fileHandling.storage import FileStorage


def getInstance():
    if PositionCalculator._instance is None:
        PositionCalculator._instance = PositionCalculator()
    return PositionCalculator._instance


class PositionCalculator:
    _instance = None

    def __init__(self):
        self.hall = SensorFactory.getInstance().getHallSensor()
        lookupTable = FileStorage.getInstance().getAngleParams()
        self._lookup = ValveOpenLookup(lookupTable.getLookupArray())

    def getPosition(self):
        rawReading = self.hall.getAveragedValue(3)
        return self._lookup.getOpenPercentageForRawReading(rawReading)
