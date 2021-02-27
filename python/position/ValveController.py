import time

from python.physical import MotorController
from python.position import PositionCalculator
from python.storage import FileStorage


def getInstance():
    if ValveController._instance is None:
        ValveController._instance = ValveController()
    return ValveController._instance


class ValveController:
    _instance = None

    def __init__(self):
        self.positionCalc = PositionCalculator.getInstance()
        self.motor = MotorController.getInstance()
        valveParams = FileStorage.getInstance().getValveParams()
        self.max = valveParams.maxOpened
        self.min = valveParams.minClosed

    def setValvePosition(self, wantedPosition):
        currentPosition = self.positionCalc.getPosition()
        fullyCloseThr = self.max * 0.02
        fullyOpenThr = self.max * 0.98

        if wantedPosition < fullyCloseThr:
            self._handleFullyClose()
        elif wantedPosition > fullyOpenThr:
            self._handleFullyOpen()
        elif currentPosition > wantedPosition:
            self._handleCloseDirection(wantedPosition)
        elif currentPosition < wantedPosition:
            self._handleOpenDirection(wantedPosition)
        self.motor.turnOff()

    def _handleFullyClose(self):
        print("Closing fully")
        self.motor.setDirectionToClose()
        self.motor.turnOn()
        while True:
            position = self.positionCalc.getPosition()
            if position < self.max * 0.1:
                break
        time.sleep(3)

    def _handleCloseDirection(self, wantedPosition):
        self.motor.setDirectionToClose()
        self.motor.turnOn()
        while True:
            position = self.positionCalc.getPosition()
            if position < wantedPosition:
                break

    def _handleFullyOpen(self):
        print("Opening fully")
        self.motor.setDirectionToOpen()
        self.motor.turnOn()
        while True:
            position = self.positionCalc.getPosition()
            if position > self.max * 0.9:
                break
        time.sleep(3)

    def _handleOpenDirection(self, wantedPosition):
        self.motor.setDirectionToOpen()
        self.motor.turnOn()
        while True:
            position = self.positionCalc.getPosition()
            if position > wantedPosition:
                break
