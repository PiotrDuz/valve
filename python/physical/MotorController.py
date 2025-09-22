import RPi.GPIO as GPIO

from python.fileHandling.storage import FileStorage


def getInstance():
    if MotorController._instance is None:
        MotorController._instance = MotorController()
    return MotorController._instance


class MotorController:
    _instance = None

    def __init__(self):
        self._pins = [24, 23]
        self._setupPins()
        self._closeDir = FileStorage.getInstance().getValveParams().closeDirection
        self._currentDir = self._closeDir


    def _setupPins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in self._pins:
            GPIO.setup(pin, GPIO.OUT)
            self._changePin(pin, GPIO.LOW)

    def setDirectionToClose(self):
        self._currentDir = self._closeDir

    def setDirectionToOpen(self):
        self._currentDir = not self._closeDir

    def turnOn(self):
        self._changePin(self._pins[int(self._currentDir)], GPIO.LOW)
        self._changePin(self._pins[int(not self._currentDir)], GPIO.HIGH)

    def turnOff(self):
        self._changePin(self._pins[int(not self._currentDir)], GPIO.LOW)

    def _changePin(self, pin: int, value: bool):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.output(pin, value)
