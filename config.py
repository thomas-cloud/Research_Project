#!/usr/bin/env python3.8
"""Used to pass data between modules."""

import queue, subprocess, time, os, logging

SUDO_PASSWD = "1234"

'''
    Create a queue variable that will be used to pass packets between modules.
    Max Size of 0, indicates infinite queue size
'''
probe_queue = queue.Queue(0) # Holds all collected packets.
device_info_dict = {} # Will hold the list of unique devices

run_staus = True

#information needed for wigle.net
wigle_encoded_token = "QUlEYzEzNGM0N2ExYmMxZTA5MDIzMmNkMGUyZmE1YjNiMTU6ZjdhMWQzZWE4ZTVkM2YyNGY3NjMzYzVlNTM5MDlkNGU="
wigle_username = "AIDc134c47a1bc1e090232cd0e2fa5b3b15"
wigle_password = "f7a1d3ea8e5d3f24f7633c5e53909d4e"


