import RPi.GPIO as GPIO

from python.fileHandling.storage import FileStorage


def getInstance():
    if MotorController._instance is None:
        MotorController._instance = MotorController()
    return MotorController._instance


class MotorController:
    _instance = None

    def __init__(self):
        self._enablePin = 13
        self._dirPin = 26
        self._setupPins()
        self._changePin(self._enablePin, GPIO.LOW)
        self._closeDir = FileStorage.getInstance().getValveParams().closeDirection
        self._openDir = not self._closeDir


    def _setupPins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._enablePin, GPIO.OUT)
        GPIO.setup(self._dirPin, GPIO.OUT)

    def setDirectionToClose(self):
        self._changePin(self._dirPin, self._closeDir)

    def setDirectionToOpen(self):
        self._changePin(self._dirPin, self._openDir)

    def turnOn(self):
        self._changePin(self._enablePin, GPIO.HIGH)

    def turnOff(self):
        self._changePin(self._enablePin, GPIO.LOW)

    def _changePin(self, pin: int, value: bool):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.output(pin, value)
