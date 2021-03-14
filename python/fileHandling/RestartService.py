import subprocess
import sys

from python.fileHandling.storage import FileStorage


def getInstance():
    if RestartService._instance is None:
        RestartService._instance = RestartService()
    return RestartService._instance


class RestartService:
    _instance = None

    def __init__(self):
        self._scriptPath = FileStorage.getInstance().getRestartScriptLocation()

    def restart(self):
        result = subprocess.run(["sudo", self._scriptPath])
        print(result.stdout)
        print(result.stderr)
        sys.stdout.flush()
        sys.stderr.flush()
