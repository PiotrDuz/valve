import time

from python.physical import MotorController
from python.position import PositionCalculator
from python.fileHandling.storage import FileStorage


def getInstance():
    if ValveController._instance is None:
        ValveController._instance = ValveController()
    return ValveController._instance


class ValveController:
    _instance = None
    _millsThreshold = 15_000

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

        if currentPosition > fullyCloseThr and wantedPosition < fullyCloseThr:
            self._handleFullyClose()
        elif currentPosition < fullyOpenThr and wantedPosition > fullyOpenThr:
            self._handleFullyOpen()
        elif currentPosition < wantedPosition * 1.05 and currentPosition > wantedPosition * 0.95:
            return
        elif currentPosition > wantedPosition:
            self._handleCloseDirection(wantedPosition)
        elif currentPosition < wantedPosition:
            self._handleOpenDirection(wantedPosition)
        self.motor.turnOff()

    def _handleFullyClose(self):
        self.motor.setDirectionToClose()
        self.motor.turnOn()
        timeStart = self._millis()
        while self._notTimeouted(timeStart):
            position = self.positionCalc.getPosition()
            if position < self.max * 0.1:
                break
        time.sleep(3)

    def _handleCloseDirection(self, wantedPosition):
        self.motor.setDirectionToClose()
        self.motor.turnOn()
        timeStart = self._millis()
        while self._notTimeouted(timeStart):
            position = self.positionCalc.getPosition()
            if position < wantedPosition:
                break

    def _handleFullyOpen(self):
        self.motor.setDirectionToOpen()
        self.motor.turnOn()
        timeStart = self._millis()
        while self._notTimeouted(timeStart):
            position = self.positionCalc.getPosition()
            if position > self.max * 0.9:
                break
        time.sleep(3)

    def _handleOpenDirection(self, wantedPosition):
        self.motor.setDirectionToOpen()
        self.motor.turnOn()
        timeStart = self._millis()
        while self._notTimeouted(timeStart):
            position = self.positionCalc.getPosition()
            if position > wantedPosition:
                break

    def _millis(self) -> float:
        return time.time() * 1000

    def _notTimeouted(self, timeStartMills):
        if(self._millis() - timeStartMills > ValveController._millsThreshold):
            return False
        return True
