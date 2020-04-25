"""
    Contains the information for device profiles.
"""

from config import device_info_dict, probe_queue
import json
from pprint import pprint
from util import save_dict

class device:
    """
        Holds the required information for a device profile
    """

    def __init__(self, mac):
        # Device mac address
        self.mac = mac
        # A list of access points the device is associated with
        

    def add_AP(self, ap_ssid, timestamp, lat=None, long=None):
        """
            Create a dict of access point info and put into a dict to hold all APs for the device
        """
        # If ap list is none, make it a dict
        if not hasattr(self, 'ap_dict'):
            self.ap_dict = {}
        if self.ap_dict is None:
            self.ap_dict = {}

        # Create a dict to hold keyed by SSID to hold timestamp
        temp = {'SSID': ap_ssid, 'TIMESTAMP': timestamp, 'LAT':lat, 'LONG':long}
        # Append the new dict to the list of known APs
        self.ap_dict[str(ap_ssid)] = temp

    def print_APs(self):
        for key in self.ap_dict:
            print(self.ap_dict[key])

    def save_device_data(self):
        with open('test_json', 'r+') as f:
            json.dump(json.dumps(self.__dict__), f)

    def load_device_data(self):
        with open('test_json', 'r') as f:
            data = json.load(f)
        return

    def __str__(self):
        return json.dumps(self.__dict__)

    def json_data(self) -> dict:
        return self.__dict__


for i in range(10):
    mac = f"TESTMAC{i}"
    temp = device(mac)
    for j in range(10):
        temp.add_AP(f"MYHOUSE{j}", 123513)
    device_info_dict[mac] = temp.json_data()

#pprint(device_info_dict)
save_dict(device_info_dict, 'devices.json')

class device_profiler:

    def __init__(self)
        # Holds the devices loaded from the probe queue
        self.devices = {}
        pass

    def profile_from_queue(self):
        # Parse all packets in the queue
        while not probe_queue.empty():
            