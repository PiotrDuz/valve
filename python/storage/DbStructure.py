from python.storage.LookupTableReadingsToPerc import LookupTableReadingsToPerc
from python.storage.ValveParams import ValveParams


class DbStructure:
    def __init__(self):
        self.lookupTable: LookupTableReadingsToPerc = LookupTableReadingsToPerc()
        self.valveParams: ValveParams = ValveParams()
