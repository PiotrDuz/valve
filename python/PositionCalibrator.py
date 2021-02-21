import math
import time
from typing import List

import numpy as np

from python import SensorFactory, MotorController
from python.storage import FileStorage
from python.storage.LookupTableReadingsToPerc import LookupTableReadingsToPerc


def getInstance():
    if PositionCalibrator._instance is None:
        PositionCalibrator._instance = PositionCalibrator()
    return PositionCalibrator._instance


class PositionCalibrator:
    _instance = None
    _maxDurationTime = 20_000
    _longAvgPeriod = 30
    _shortAvgPeriod = 3

    def __init__(self):
        self.storage = FileStorage.getInstance()
        self.hall = SensorFactory.getInstance().getHallSensor()
        self.motor = MotorController.getInstance()

    def calibrate(self):
        print("Calibration process started")
        readings = self._getReadingsOpeningTheValve()
        print("Collected " + str(len(readings)) + " points.")

        smoothedReadings = self._smoothArray(readings, 4)
        smoothedAndCutReadings = self._discardFlatBeginningAndEnd(smoothedReadings, 50)
        print("Created smoothed array of " + str(len(smoothedAndCutReadings)) + " points.")

        percentages = self._splitPercentagesRangeIntoPoints(len(smoothedAndCutReadings))
        print("Created range between " + str(percentages[0]) + " : " +
              str(percentages[len(percentages) - 1]) + " of points size " + str(len(percentages)))

        readingsToPercentageSorted2dArray = self._produceAndSort2dArray(smoothedAndCutReadings, percentages)
        self.storage.setAngleParams(LookupTableReadingsToPerc(readingsToPercentageSorted2dArray))

    def _produceAndSort2dArray(self, readings: List, percentages: List) -> np.ndarray:
        array2D = np.vstack((readings, percentages)).T
        return array2D[array2D[:, 0].argsort()]

    def _discardFlatBeginningAndEnd(self, array: List,
                                    avg: int):  # when difference between SMA and curve is small, treat it like flat curve
        movingAverage = self._computeMovingAverage(array, avg)
        differences = self._computeDifferences(array, movingAverage)
        endCutoffIdx, startCutoffIdx = self._computeCutoffPoints(differences)
        return array[startCutoffIdx:endCutoffIdx + 1]

    def _computeCutoffPoints(self, differences):
        size = len(differences)
        midPoint = int(size / 2)
        startCutoffIdx = 0
        endCutoffIdx = size - 1
        diffThreshold = self._average(differences[midPoint - 2: midPoint + 3]) * 0.15
        for x in range(midPoint, 0, -1):
            if differences[x] < diffThreshold:
                startCutoffIdx = x
                break
        for x in range(midPoint, size):
            if differences[x] < diffThreshold:
                endCutoffIdx = x
                break
        return endCutoffIdx, startCutoffIdx

    def _computeDifferences(self, array, movingAverage):
        differences = []
        size = len(array)
        for x in range(0, size):  #
            differences.append(math.fabs(movingAverage[x] - array[x]))
        return differences

    def _computeMovingAverage(self, array, avg):
        size = len(array)
        avgValidIndex = avg - 1
        movingAverage = []
        for x in range(0, size):
            if x < avgValidIndex:
                movingAverage.append(array[x])
            else:
                movingAverage.append(self._average(array[x - avgValidIndex:x + 1]))
        return movingAverage

    def _smoothArray(self, readings: List, leftRightAvg: int) -> List:
        origSize = len(readings)
        newReadings = [readings[0]]
        for x in range(0, origSize):
            if x > leftRightAvg - 1 and x < origSize - leftRightAvg:
                newReadings.append(self._average(readings[x - leftRightAvg:x + leftRightAvg + 1]))
        return newReadings

    def _average(self, lst: List):
        return sum(lst) / len(lst)

    def _getReadingsOpeningTheValve(self) -> List:
        readings = []
        longAvg = [0 for x in range(PositionCalibrator._longAvgPeriod)]
        shortAvg = [0 for x in range(PositionCalibrator._shortAvgPeriod)]
        timeStart = self._millis()
        timeOfLastSleep = timeStart

        self.motor.setDirectionToOpen()
        self.motor.turnOn()
        time.sleep(0.005)  # little more for starting
        while self._millis() - timeStart < PositionCalibrator._maxDurationTime:  # prevent infinite loop
            if self._millis() - timeOfLastSleep > 2:
                timeOfLastSleep = self._millis()
            else:
                continue
            reading = self.hall.getValue()
            readings.append(reading)
            self._manageAverage(shortAvg, reading)
            self._manageAverage(longAvg, reading)
            if self._hasOneSecondPassedToCompare(timeStart):
                if self._areArraysAveragesCloseEnough(longAvg, shortAvg):
                    break
        self.motor.turnOff()
        return readings[:-PositionCalibrator._longAvgPeriod]

    def _millis(self) -> float:
        return time.time() * 1000

    def _areArraysAveragesCloseEnough(self, val1: List, val2: List) -> bool:
        val1Avg = np.mean(val1)
        val2Avg = np.mean(val2)
        return math.fabs(val1Avg - val2Avg) / val1Avg < 3.0e-15

    def _manageAverage(self, avg: List, value: float):
        avg.append(value)
        avg.pop(0)

    def _hasOneSecondPassedToCompare(self, lastComparisionTime):
        return self._millis() - lastComparisionTime > 1000

    def _splitPercentagesRangeIntoPoints(self, nb) -> List:
        end = self.storage.getValveParams().maxOpened
        start = self.storage.getValveParams().minClosed
        step = (end - start) / (nb - 1)
        createdRange = [start]
        value = start
        for i in range(1, nb):
            value = value + step
            createdRange.append(value)
        return createdRange
