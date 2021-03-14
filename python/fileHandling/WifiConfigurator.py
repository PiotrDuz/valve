import subprocess
import sys

from python.fileHandling.storage import FileStorage


def getInstance():
    if WifiConfigurator._instance is None:
        WifiConfigurator._instance = WifiConfigurator()
    return WifiConfigurator._instance


class WifiConfigurator:
    _instance = None

    def __init__(self):
        self._scriptPath = FileStorage.getInstance().getSetWififScriptLocation()

    def setWifi(self, ssid: str, password: str):
        result = subprocess.run(["sudo", self._scriptPath, ssid, password, ";", "history", "-cw"])
        print(result.stdout)
        print(result.stderr)
        sys.stdout.flush()
        sys.stderr.flush()
