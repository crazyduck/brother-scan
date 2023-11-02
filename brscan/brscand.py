#!/usr/bin/env python3
"""
# (C) 2013 Francois Cauwe
# (C) 2015-2018 Esben Haabendal
# (C) 2023 Maximilian Krause
"""


# Global libs
import sys
import time
import threading
import argparse
import socket
import functools
import yaml

from yaml import CLoader

# Private libs
from . import listen
from . import snmp

# activate flush option in print cmd to see it in docker logs
myprint = functools.partial(print, flush=True)


def main():
    """ Main class of module which is callable """
    parser = argparse.ArgumentParser(
        description='Brother network scanner server')
    parser.add_argument('bind_addr', metavar='BIND_ADDR',
                        type=str,
                        help='IP/host to bind UDP socket to')
    parser.add_argument('-p', '--bind-port', metavar='PORT',
                        type=int, default=54925,
                        help='UDP port number to bind UDP socket to')
    parser.add_argument('-A', '--advertise-addr', metavar='ADDR',
                        type=str, default=None,
                        help='IP/host to advertise to scanner')
    parser.add_argument('-P', '--advertise-port', metavar='PORT',
                        type=int, default=None,
                        help='UDP port number to advertise to scanner')
    parser.add_argument('scanner_addr', metavar='SCANNER_ADDR',
                        type=str,
                        help='IP address of scanner')
    parser.add_argument('-c', '--config', metavar='FILE',
                        type=str, default='brother-scan.yaml',
                        help='Configuration file')
    args = parser.parse_args()
    if args.advertise_addr is None:
        args.advertise_addr = args.bind_addr
    if args.advertise_port is None:
        args.advertise_port = args.bind_port

    # Resolv hosts
    args.bind_addr = socket.gethostbyname(args.bind_addr)
    args.advertise_addr = socket.gethostbyname(args.advertise_addr)
    args.scanner_addr = socket.gethostbyname(args.scanner_addr)

    # Loading global configuration
    try:
        with open(args.config, encoding='utf-8') as configfile:
            config = yaml.load(configfile, Loader=CLoader)
            myprint(f'Config loaded: {args.config}')
    except FileNotFoundError as e:
        myprint(f'Error: {e.strerror}: {e.filename}')
        sys.exit(1)

    # Start listen Thread
    listen_thread = threading.Thread(target=listen.launch, args=(args, config))
    listen_thread.start()
    time.sleep(1)

    # Start Snmp
    snmp_thread = threading.Thread(target=snmp.launch, args=(args, config))
    snmp_thread.start()

    # Wait for closing
    snmp_thread.join()
    listen_thread.join()


if __name__ == '__main__':
    main()
