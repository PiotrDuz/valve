import subprocess

from python.fileHandling.storage import FileStorage

def getInstance():
    if AccessPoint._instance is None:
        AccessPoint._instance = AccessPoint()
    return AccessPoint._instance

class AccessPoint:
    _instance = None
    def __init__(self):
        self._location = FileStorage.getInstance().getAccessPointScriptLocation()

    def switchToAccessPoint(self):
        result = subprocess.run([self._location, "start"])
        print(result.stdout)
        print(result.stderr)