import pickle
from pathlib import Path

from python.fileHandling.storage.DbStructure import DbStructure
from python.fileHandling.storage.LookupTableReadingsToPerc import LookupTableReadingsToPerc
from python.fileHandling.storage.MqttSettings import MqttSettings
from python.fileHandling.storage.ValveParams import ValveParams

# _filePath = Path(r"C:\Users\00pit\PROJECTS\data.dat")


_filePath = Path("/home/pi/db/data.dat")


def getInstance():
    if FileStorage._instance is None:
        FileStorage._instance = FileStorage()
    return FileStorage._instance


class FileStorage:
    _instance = None

    def __init__(self):
        self._data: DbStructure = DbStructure()
        if _filePath.exists():
            with open(_filePath, 'rb') as file:
                self._data: DbStructure = pickle.load(file)

    def getRestartScriptLocation(self):
        return self._data.restartScriptLocation

    def getAccessPointScriptLocation(self):
        return self._data.accessPointScriptLocation

    def getSetWififScriptLocation(self) -> str:
        return self._data.wifiScriptPath

    def getAngleParams(self) -> LookupTableReadingsToPerc:
        return self._data.lookupTable

    def getValveParams(self) -> ValveParams:
        return self._data.valveParams

    def setAngleParams(self, params: LookupTableReadingsToPerc):
        self._data.lookupTable = params
        self.save()

    def setMqttSettings(self, settings: MqttSettings):
        self._data.mqttSettings = settings
        self.save()

    def getMqttSettings(self) -> MqttSettings:
        return self._data.mqttSettings

    def save(self):
        with open(_filePath, 'wb') as fileWrite:
            pickle.dump(self._data, fileWrite, 4)
