from RPi import GPIO


def getInstance():
    if Button._instance is None:
        Button._instance = Button()
    return Button._instance


class Button:
    _instance = None

    def __init__(self):
        self._pin = 16
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def isNotPressed(self):
        state = GPIO.input(self._pin)
        return state == True
