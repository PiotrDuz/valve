import numpy as np


class ValveOpenLookup:
    def __init__(self, array: np.ndarray):
        self._array = array

    def getOpenPercentageForRawReading(self, reading: float) -> float:
        idx = np.searchsorted(self._array[:, 0], reading, side="left")
        if idx != 0:
            idx = idx - 1
        return self._array[idx, 1]