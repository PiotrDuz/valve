from numpy import ndarray


class LookupTableReadingsToPerc:
    def __init__(self, array: ndarray = None):
        self.array: ndarray = array

    def setLookupArray(self, array: ndarray):
        self.array = array

    def getLookupArray(self):
        return self.array
