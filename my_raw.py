#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Raw probe request viewer.
"""

from csv import writer

from probequest.probe_request_sniffer import ProbeRequestSniffer
from config import probe_queue, probe_count

class RawProbeRequestViewer:
    """
    Displays the raw probe requests passing nearby the Wi-Fi interface.
    """

    def __init__(self, config):
        # Set the output file
        self.output = config.output_file

        if self.output is not None:
            outfile = writer(self.output, delimiter=";")

            def write_csv(probe_req):
                outfile.writerow([
                    probe_req.timestamp,
                    probe_req.s_mac,
                    probe_req.s_mac_oui,
                    probe_req.essid
                ])
        else:
            # If an output file is not specified, Push item to the queue.    
            def enqueue_probe(probe_req):
                # Enqueue the packet
                probe_queue.put(probe_req)
                # Increase the Packet count by 1
                #probe_count += 1


            #write_csv = lambda *args: None  # noqa: E731

        def display_probe_req(probe_req):
            print(f'Test {probe_req}')

        config.display_func = display_probe_req
        config.storage_func = enqueue_probe

        self.sniffer = ProbeRequestSniffer(config)

    def start(self):
        """
        Starts the probe request sniffer.
        """

        self.sniffer.start()

    def stop(self):
        """
        Stops the probe request sniffer.
        """

        self.sniffer.stop()

        if self.output is not None:
            self.output.close()
