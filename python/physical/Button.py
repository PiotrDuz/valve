from RPi import GPIO


def getInstance():
    if Button._instance is None:
        Button._instance = Button()
    return Button._instance


class Button:
    _instance = None
    _pressedState = False

    def __init__(self):
        self._pin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def isPressed(self):
        state = GPIO.input(self._pin)
        return state == Button._pressedState
