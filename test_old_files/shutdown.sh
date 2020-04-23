#!/bin/sh

#stop the aimon monitor mode
echo "---STOPPING MONITOR ON INTERFACE $1"
airmon-ng stop wlan0

#restart the network manager
echo "---RESTARTING NETWORK-MANAGER"
service network-manager restart
echo "---NETWORK MANAGER RESTARTED. PRESS ENTER"