"""
    Overwriting of the Probequest classes used for probe sniffing, parsing, and handling
"""


from probequest.ui.raw import RawProbeRequestViewer
from config import probe_queue

class My_RawProbeRequestViewer(RawProbeRequestViewer):
    """
        Custom RawProbeRequest Viewer Class

        Changed the storage and display functions for probe requests
        Changed the ProbeRequestSniffer class to My_ProbeRequestSniffer class.
    """
    def __init__(self, config):

        def store_probe(probe_req):
            # Enqueue the packet
            probe_queue.put(probe_req)

        def print_probe(probe_req):
            print(probe_req)

        config.display_func = print_probe
        config.storage_func = store_probe

        self.sniffer = My_ProbeRequestSniffer(config)

    def stop(self):
        """
            Custom Method. Stops the probe request sniffer.

            Removed the check for an output file.
        """

        self.sniffer.stop()



from probequest.probe_request_sniffer import ProbeRequestSniffer
class My_ProbeRequestSniffer(ProbeRequestSniffer):
    """
        Custom Probe Request Sniffer Class

        The Probe request parser object has been replaced with My_ProbeRequestParser
    """
    def new_parser(self):
        """
        Creates a new custom parsing thread.

        Replaced the ProbeRequestParser class with My_ProbeRequestParser class, in order to get the proper information
        """

        self.parser = My_ProbeRequestParser(
            self.config,
            self.new_packets
        )

from scapy.layers.dot11 import RadioTap, Dot11ProbeReq
from probequest.probe_request_parser import ProbeRequestParser
class My_ProbeRequestParser(ProbeRequestParser):
    """
        Custom ProbeRequestParser Class

        The ProbeRequest object has been replaced with My_ProbeRequest Custom Class
    """
    @staticmethod
    def parse(packet):
        """
            Customized Packet Parsing function
        """

        try:
            if packet.haslayer(Dot11ProbeReq):
                timestamp = packet.getlayer(RadioTap).time
                s_mac = packet.getlayer(RadioTap).addr2
                # Get the destination MAC address. May be in the DOT11 frame
                d_mac = packet.getlayer(RadioTap).addr1
                essid = packet.getlayer(Dot11ProbeReq).info.decode("utf-8")

                return My_ProbeRequest(timestamp, d_mac, s_mac, essid)

            return None
        except UnicodeDecodeError:
            # The ESSID is not a valid UTF-8 string.
            return None


from probequest.probe_request import ProbeRequest
class My_ProbeRequest(ProbeRequest):
    """
        Custom ProbeRequest Class

        The Source MAC has been added to the parser as s_mac
        and the __str__ function has been replaced to return custom information
    """

    def __init__(self, timestamp, d_mac, s_mac, essid):
        super().__init__(timestamp, s_mac, essid)
        self.d_mac = d_mac

    def __str__(self):
        return f'{self.timestamp},{self.d_mac},{self.s_mac},{self.essid}'