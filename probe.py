#!/usr/bin/env python3.8
""""Included the functionality to prepare the wireless card for logging, and start the logging service"""


#import the Scapy library to parse the packets
from scapy.all import *
import os, subprocess, signal, threading
#import the packet queue from the config module
from util import is_root, countdown
from time import sleep

from config import probe_queue


class probe_parser:
    """Parses Wireless packets and places probe-requests into a queue for processing 

        This class adds the functionality to parse wireless packet data and 
        process deteceted probe requests.
        This class will also ensure the wireless interface is set in monitor mode, and is unmanaged
    """

    def __init__(self, interface):

        self.interface = interface
        # Run the startup procedures
        '''
        startup_thread = threading.Thread(target=self.startup)
        startup_thread.start()    
        startup_thread.join()
        '''
        self.startup()
        return

    def __del__(self):
        """ Do Cleanup"""
        # Run cleanup scripts.
        #self.shutdown()
        return
    
    def startup(self):
        """ Prepares the Wireless interface for sniffing
        Sets the interface into monitor mode and stops sets the interface into unmaged status
        
        """
        # Check if process is running as root
        is_root()
        # Kill Processes that are managing the interface
        logging.info("Killing Problem Processes")
        # Check for problem proceses.
        proc_output = subprocess.check_output(['airmon-ng', 'check'])

        # Check if kill needs to be run
        if 'Found' in str(proc_output):
            subprocess.check_output(['airmon-ng', 'check', 'kill'])
            t = countdown("Killing Problem Processes", 5)

        
        # Set the interface into monitor mode
        logging.info("+Starting Interface: Monitor Mode")
        proc_output = subprocess.check_output(['airmon-ng', 'start', str(self.interface)])
        t = countdown("Setting interface to monitor mode", 5)
        # Check for success
        if 'enabled' in str(proc_output):
            logging.debug(f'Monitor mode enabled: {self.interface}')
        else:
            # Exit if failed
            logging.critical("Unable to put interface into monitor mode.\n Exiting...")
            exit(1)

        # Start channel hopping on 2.4 and 5 Ghz 
        logging.info("+Starting Channel Hopping")
        self.airodump_proc = subprocess.Popen(['airodump-ng', '-i', str(self.interface), '-b', 'abg'], stdout=subprocess.DEVNULL)
        #Wait for the program to start
        t = countdown("Launching Airodump-ng", 5)
        
        return
    
    def shutdown(self):
        """ Returns the interface to managed mode, and terminates supporing networking programs"""
        # Terminate the Airodump process
        if hasattr(self, 'airodump_proc'):
            os.kill(self.airodump_proc.pid, signal.SIGTERM)
        else:
            logging.debug("No Airodump-ng Process to terminate")
        
        # Take the interface out of promiscuious mode
        logging.debug("+Returning Interface to Managed Mode")
        proc_output = subprocess.check_output(['airmon-ng', 'stop', 'wlan0'])
        if 'disabled' in str(proc_output):
            logging.debug(f"Monitor mode disabled: {self.interface}")
        
        # Restart the network manager servcice 
        logging.debug("+Restarting Network-manager")
        subprocess.check_output(['service', 'network-manager','start'])

        return

    
    def start_capture(self, time):
        """Starts the probequest thread"""
        # Create the thread object
        self.probequest_thread = threading.Thread(target=self.capture, args=(time))
        # Start the capturing thread
        self.probequest_thread.start()
        # Join the thread
        self.probequest_thread.join()

    def capture(self, runtime):
        """ This Function will start the capture of probe requests
            Captured probe requests will be stored in the probe_queue queue.
        """


        from sys import exit as sys_exit
        from probequest.probe_request_sniffer import ProbeRequestSniffer
        from util import get_arg_parser
        from config import probe_queue

        from probequest.config import Mode
        from probe_config import My_Config

        # Create a Config object
        new_config = My_Config()
        
        # Manually Set the Config Options
        new_config.interface = str(self.interface) #interface to capture from
        new_config.runtime = runtime

        print(new_config.interface)
        # Do all of the sniffing stuff
        
        from time import sleep
        from probe_handler import My_RawProbeRequestViewer

        try:
            print("[*] Start sniffing probe requests...")
            # Start the viewer module
            raw_viewer = My_RawProbeRequestViewer(new_config)
            raw_viewer.start()

            while new_config.runtime > 0:
                sleep(1)
                logging.debug(f'Probe_queue Count {probe_queue.qsize()}')
                logging.debug(f"runtime: {new_config.runtime}")
                new_config.runtime -= 1
            # Stop the Sniffing of packets
            raw_viewer.stop()
        except OSError:
            raw_viewer.stop()
            sys_exit(
                "[!] Interface {interface} doesn't exist".format(
                    interface=config.interface
                )
            )
        
    def enqueue_probe(self, probe_req):
        # Enqueue the packet
        probe_queue.put(probe_req)
        # Increase the Packet count by 1
        #probe_count += 1


if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    # Create a new parser Object
    temp = probe_parser('wlan0')
    # Start Capturing probe requests 
    temp.capture(60) #Replace with temp.start_capture()
    temp.shutdown()
    print("-----SCRIPT END-----")
    
    