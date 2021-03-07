from python.fileHandling.storage.LookupTableReadingsToPerc import LookupTableReadingsToPerc
from python.fileHandling.storage.MqttSettings import MqttSettings
from python.fileHandling.storage.ValveParams import ValveParams


class DbStructure:
    def __init__(self):
        self.lookupTable: LookupTableReadingsToPerc = LookupTableReadingsToPerc()
        self.valveParams: ValveParams = ValveParams()
        self.mqttSettings: MqttSettings = MqttSettings()
        self.wifiScriptPath: str = "/usr/sbin/setWifi.sh"
        self.accessPointScriptLocation: str = "/home/pi/hotspot/hotspot"
        self.restartScriptLocation: str = "/usr/sbin/restartValve.sh"
        self.startAccessPointScriptLocation: str = "/usr/sbin/restartValve.sh"
