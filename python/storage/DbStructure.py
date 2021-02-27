from python.storage.LookupTableReadingsToPerc import LookupTableReadingsToPerc
from python.storage.MqttSettings import MqttSettings
from python.storage.ValveParams import ValveParams


class DbStructure:
    def __init__(self):
        self.lookupTable: LookupTableReadingsToPerc = LookupTableReadingsToPerc()
        self.valveParams: ValveParams = ValveParams()
        self.mqttSettings: MqttSettings = MqttSettings()
