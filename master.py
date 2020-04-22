#!/usr/bin/env python3.8
"""Wireless device profiling script.

    Author: Thomas Cloud
    Date: 4/11/2020
    Description: 
        This script will monitor the conencted wireless interface, and
        create device profiles for each wireless device connected.
        It logs a list of wireless networks for each individual device, and 
        geolocates them.
"""

import probe, logging, subprocess, os

#import the packet queue from the config module
from config import probe_queue




#temp = my_probe.probe_parser("wlan0")

class master:
    """Master interface for device profiling

        Utilities for creating device profiles based on probe request data
    """

    '''
        This function will run the startup.sh script to prepare the interface
    '''
    def __init__(self, interface, **kwargs):
        """Creates the object, and sets the config options if specified"""
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("MASTER OBJECT CREATED")

        #check if the script is running as root
        #self.is_root()

        # Set the config options
        self.interface = interface
        self.config(**kwargs)
        return

    
    def __del__(self):
        logging.debug("MASTER OBJECT FREED")
        #with open("shutdown_log.txt", 'w') as f:
        #    process = subprocess.Popen(['./startup.sh'], stdout=f)
        return

    def config(self, **kwargs):
        """Sets the basic configuration information"""
        for key, value in kwargs.items():
            if key == "iface":
                logging.debug(f"Iterface set to: {value}")
                self.interface = value
            elif key == "timeout":
                logging.debug(f"Timeout set to: {value}")
                self.timeout = int(value)


    def start_collecting(self):
        """Starts the collection of packets"""
        self.collector = probe.probe_parser(self.interface)
        return



temp1 = master("wlan0", timeout=10)

