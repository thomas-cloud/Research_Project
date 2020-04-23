"""
    Contains the information for device profiles.
"""


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
        if self.ap_list is None or not hasattr(self, 'ap_list'):
            self.ap_list = {}
        # Create a dict to hold keyed by SSID to hold timestamp
        temp = {'SSID': ap_ssid, 'TIMESTAMP': timestamp, 'LAT':lat, 'LONG':long}
        # Append the new dict to the list of known APs
        self.ap_list[str(ap_ssid)] = temp

    def print_APs(self):
        for key in self.ap_list:
            print(self.ap_list[key])



    