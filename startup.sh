#!/bin/sh
echo "---STARTING STARTUP.SH"
#kill the proceses that may put the interface back into managed mode
echo "---KILLING PROBLEM PROCESSES"
airmon-ng check
airmon-ng check kill

#put wlan0 in monitor mode
echo "---ENABLE MONITOR MODE ON INTERFACE $1"
airmon-ng start "$1"

#start airodump-ng to hop channels 
echo "---STARTING CHANNEL HOPPING"
airodump-ng "$1" -b abg

