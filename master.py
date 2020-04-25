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
from probe import probe_parser
from util import print_queue



#temp = my_probe.probe_parser("wlan0")

class master:
    """Master interface for device profiling

        Utilities for creating device profiles based on probe request data
    """

    '''
        This function will run the startup.sh script to prepare the interface
    '''
    def __init__(self, **kwargs):
        """Creates the object, and sets the config options if specified"""
        #logging.basicConfig(level=logging.DEBUG)
        logging.debug("MASTER OBJECT CREATED")

        #check if the script is running as root
        #self.is_root()

        # Set the config options
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
            if key == "interface":
                logging.debug(f"Iterface set to: {value}")
                self.interface = value
            elif key == "capturetime":
                logging.debug(f"Capturetime set to: {value}")
                self.capturetime = int(value)

        if not hasattr(self, 'interface'):
            print("**Error, Requires Interface")
            exit(1)
        elif not hasattr(self, 'capturetime'):
            logging.debug("Capturetime set to default: 300")
            capturetime = 300


    def start_collecting(self):
        """Starts the collection of packets"""
        # Create the probe parsing object
        self.probe = probe_parser(self.interface)
        # Start capturing probes
        self.probe.capture(self.capturetime)
        # Shutdown the Capture
        self.probe.shutdown()

        return

    def run(self):
        # Start collecting probes in the queue
        self.start_collecting()
        # Print the queue
        print_queue(probe_queue)
'''
        # Parse the packets into individual Files
        self.parse()
        self.geolocate()
'''


temp = master(interface="wlan0", capturetime=60)
temp.run()
print("SCRIPT END")

