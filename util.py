import threading

def is_root():
    """
        This function checks for the privledge levels of the script.
        If it is not running as root, the script will exit.
    """
    from os import getuid
    import logging
    #check if script is running as root
    if getuid() != 0:
        logging.error(f"**ERROR - Script requires elevated privledges. UID={os.getuid()}")
        exit(1)
    return

class countdown:
    """ Countdown timer class"""
    
    def __init__(self, name, seconds, n=1):
        self.name = name
        self.seconds = seconds
        self.n = n
        """Prints a countdown timer to the screen starting at seconds, and decremented by n """
        from time import sleep
        while(self.seconds > 0):
            print(f'{self.name}: {self.seconds} ', end='\r')
            sleep(self.n)
            self.seconds -= self.n
        print(f'{self.name}, Done.')


def print_queue(pQueue):
    print("Printing Queue")
    while not pQueue.empty():
        print(pQueue.get())


def get_arg_parser():
    """
    Returns the argument parser.
    """

    from argparse import ArgumentParser, FileType

    from probequest.config import Config, Mode
    from probequest.version import VERSION

    arg_parser = ArgumentParser(
        description="Toolkit for Playing with Wi-Fi Probe Requests"
    )
    arg_parser.add_argument(
        "--debug", action="store_true",
        dest="debug",
        help="debug mode"
    )
    arg_parser.add_argument(
        "--fake", action="store_true",
        dest="fake",
        help="display only fake ESSIDs")
    arg_parser.add_argument(
        "-i", "--interface",
        required=True,
        dest="interface",
        help="wireless interface to use (must be in monitor mode)"
    )
    arg_parser.add_argument(
        "--ignore-case", action="store_true",
        dest="ignore_case",
        help="ignore case distinctions in the regex pattern (default: false)"
    )
    arg_parser.add_argument(
        "--mode",
        type=Mode, choices=Mode.__members__.values(),
        dest="mode",
        help="set the mode to use"
    )
    arg_parser.add_argument(
        "-o", "--output",
        type=FileType("a"),
        dest="output_file",
        help="output file to save the captured data (CSV format)"
    )
    arg_parser.add_argument("--version", action="version", version=VERSION)
    arg_parser.set_defaults(debug=False)
    arg_parser.set_defaults(fake=False)
    arg_parser.set_defaults(ignore_case=False)
    arg_parser.set_defaults(mode=Mode.RAW)

    essid_arguments = arg_parser.add_mutually_exclusive_group()
    essid_arguments.add_argument(
        "-e", "--essid",
        nargs="+",
        dest="essid_filters",
        help="ESSID of the APs to filter (space-separated list)"
    )
    essid_arguments.add_argument(
        "-r", "--regex",
        dest="essid_regex",
        help="regex to filter the ESSIDs"
    )

    station_arguments = arg_parser.add_mutually_exclusive_group()
    station_arguments.add_argument(
        "--exclude",
        nargs="+",
        dest="mac_exclusions",
        help="MAC addresses of the stations to exclude (space-separated list)"
    )
    station_arguments.add_argument(
        "-s", "--station",
        nargs="+",
        dest="mac_filters",
        help="MAC addresses of the stations to filter (space-separated list)"
    )

    return arg_parser


def save_dict(data:dict, filename:str):
    with open(filename, 'w') as f:
        json_string = json.dumps(devices)
        json.dump(json_string, f)



if __name__ == '__main__':
    t = timer("Test Timer", 5, 0.5)
    print("Starting")
    t.start()
    print("Stopping")
    t.stop()
    print("Stopped")