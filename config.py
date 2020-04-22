#!/usr/bin/env python3.8
"""Used to pass data between modules."""

import queue, subprocess, time, os, logging

SUDO_PASSWD = "1234"

'''
    Create a queue variable that will be used to pass packets between modules.
    Max Size of 0, indicates infinite queue size
'''
probe_queue = queue.Queue(0)



probe_count = 0


