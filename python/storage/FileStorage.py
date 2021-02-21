import pickle
from pathlib import Path

from python.storage.DbStructure import DbStructure
from python.storage.LookupTableReadingsToPerc import LookupTableReadingsToPerc
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
        self.data = DbStructure()
        if _filePath.exists():
            with open(_filePath, 'rb') as file:
                self.data: DbStructure = pickle.load(file)

    def getAngleParams(self) -> LookupTableReadingsToPerc:
        return self.data.lookupTable

    def getValveParams(self) -> ValveParams:
        return self.data.valveParams

    def setAngleParams(self, params: LookupTableReadingsToPerc):
        self.data.lookupTable = params
        self.save()

    def save(self):
        with open(_filePath, 'wb') as fileWrite:
            pickle.dump(self.data, fileWrite, 4)
