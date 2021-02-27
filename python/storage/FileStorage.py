import pickle
from pathlib import Path

from python.storage.DbStructure import DbStructure
from python.storage.LookupTableReadingsToPerc import LookupTableReadingsToPerc
from python.storage.MqttSettings import MqttSettings
from python.storage.ValveParams import ValveParams

# _filePath = Path(r"C:\Users\00pit\PROJECTS\data.dat")


_filePath = Path("/home/pi/db/data.dat")


def getInstance():
    if FileStorage._instance is None:
        FileStorage._instance = FileStorage()
    return FileStorage._instance


class FileStorage:
    _instance = None

    def __init__(self):
        self._data = DbStructure()
        if _filePath.exists():
            with open(_filePath, 'rb') as file:
                self._data: DbStructure = pickle.load(file)

    def getAngleParams(self) -> LookupTableReadingsToPerc:
        return self._data.lookupTable

    def getValveParams(self) -> ValveParams:
        return self._data.valveParams

    def setAngleParams(self, params: LookupTableReadingsToPerc):
        self._data.lookupTable = params
        self.save()

    def getMqttSettings(self) -> MqttSettings:
        return self._data.mqttSettings

    def save(self):
        with open(_filePath, 'wb') as fileWrite:
            pickle.dump(self._data, fileWrite, 4)
