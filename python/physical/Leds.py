from RPi import GPIO


def getInstance():
    if Leds._instance is None:
        Leds._instance = Leds()
    return Leds._instance

class Leds:
    _instance = None
    def __init__(self):
        self._red = 5
        self._green = 6
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._red, GPIO.OUT)
        GPIO.setup(self._green, GPIO.OUT)
        GPIO.output(self._red, False)
        GPIO.output(self._green, False)

    def setGreenOn(self):
        self._changePin(self._green, True)

    def setGreenOff(self):
        self._changePin(self._green, False)

    def setRedOn(self):
        self._changePin(self._red, True)

    def setRedOff(self):
        self._changePin(self._red, False)

    def _changePin(self, pin: int, value: bool):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.output(pin, value)
