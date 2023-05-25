#!/usr/bin/env python3

from __future__ import print_function

import sys
import argparse
import subprocess

import signal

proc = None

def signal_handler(signum, frame):
    global proc
    proc.terminate()
    exit(1)

signal.signal(signal.SIGTERM, signal_handler)

# initialized = False
channel = 15

CTRL_ARG_CHANNEL = 1

"""
This code has been taken from http://stackoverflow.com/questions/5943249/python-argparse-and-controlling-overriding-the-exit-status-code - originally developed by Rob Cowie http://stackoverflow.com/users/46690/rob-cowie
"""
class ArgumentParser(argparse.ArgumentParser):
    def _get_action_from_name(self, name):
        """Given a name, get the Action instance registered with this parser.
        If only it were made available in the ArgumentError object. It is
        passed as it's first arg...
        """
        container = self._actions
        if name is None:
            return None
        for action in container:
            if '/'.join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action

    def error(self, message):
        exc = sys.exc_info()[1]
        if exc:
            exc.argument = self._get_action_from_name(exc.argument_name)
            raise exc
        super(ArgumentParser, self).error(message)

### EXTCAP FUNCTIONALITY

"""@brief Extcap configuration
This method prints the extcap configuration, which will be picked up by the
interface in Wireshark to present a interface specific configuration for
this extcap plugin
"""
def extcap_config(interface, option):
    args = []

    args.append((0, '--channel', 'Channel', 'Channel', 'unsigned', '{range=11,25}{required=true}'))

    if len(option) <= 0:
        for arg in args:
            print("arg {number=%d}{call=%s}{display=%s}{tooltip=%s}{type=%s}%s" % arg)


def extcap_version():
    print("extcap {version=1.0}{display=CC2531 sniffer}")


def extcap_interfaces():
    print("extcap {version=1.0}{display=CC2531 sniffer}")
    print("interface {value=cc2531}{display=IEEE 802.15.4 capture}")
    # print("control {number=%d}{type=selector}{display=Channel}{tooltip=IEEE 802.15.4 channel}" % CTRL_ARG_CHANNEL)

    # for ch in range(11, 26):
    #     print("value {control=%d}{value=%d}{display=%d}" % (CTRL_ARG_CHANNEL, ch, ch))


def extcap_dlts(interface):
    if interface == 'cc2531':
        print("dlt {number=147}{name=USER0}{display=CC2531 DLT}")


def extcap_capture(interface, fifo, in_channel):
    global channel, proc
    channel = in_channel if in_channel in range(11, 26) else 15

    proc = subprocess.Popen([f'whsniff -c {channel} -p {fifo}'], shell=True)

    proc.wait()


def extcap_close_fifo(fifo):
    # This is apparently needed to workaround an issue on Windows/macOS
    # where the message cannot be read. (really?)
    fh = open(fifo, 'wb', 0)
    fh.close()

####

def usage():
    print("Usage: %s <--extcap-interfaces | --extcap-dlts | --extcap-interface | --extcap-config | --capture | --extcap-capture-filter | --fifo>" % sys.argv[0] )

if __name__ == '__main__':
    interface = ""
    option = ""

    # Capture options
    delay = 0
    message = ""
    ts = 0

    parser = ArgumentParser(
            prog="Extcap Example",
            description="Extcap example program for Python"
            )
    # Extcap Arguments
    parser.add_argument("--capture", help="Start the capture routine", action="store_true" )
    parser.add_argument("--extcap-interfaces", help="Provide a list of interfaces to capture from", action="store_true")
    parser.add_argument("--extcap-interface", help="Provide the interface to capture from")
    parser.add_argument("--extcap-dlts", help="Provide a list of dlts for the given interface", action="store_true")
    parser.add_argument("--extcap-config", help="Provide a list of configurations for the given interface", action="store_true")
    parser.add_argument("--extcap-capture-filter", help="Used together with capture to provide a capture filter")
    parser.add_argument("--fifo", help="Use together with capture to provide the fifo to dump data to")
    parser.add_argument("--extcap-version", help="Shows the version of this utility", nargs='?', default="")
    parser.add_argument("--extcap-reload-option", help="Reload elements for the given option")

    # Interface Arguments
    parser.add_argument("--port", help="Port", nargs='?', default="")
    parser.add_argument("--channel", help="Channel", type=int, default=0, choices=range(11, 26))

    try:
        args, unknown = parser.parse_known_args()
    except argparse.ArgumentError as exc:
        print("%s: %s" % (exc.argument.dest, exc.message), file=sys.stderr)
        fifo_found = 0
        fifo = ""
        for arg in sys.argv:
            if arg == "--fifo" or arg == "--extcap-fifo":
                fifo_found = 1
            elif fifo_found == 1:
                fifo = arg
                break
        extcap_close_fifo(fifo)
        sys.exit(1)

    if len(sys.argv) <= 1:
        parser.exit("No arguments given!")

    if args.extcap_version and not args.extcap_interfaces:
        extcap_version()
        sys.exit(0)

    if not args.extcap_interfaces and args.extcap_interface is None:
        parser.exit("An interface must be provided or the selection must be displayed")

    if args.extcap_interfaces or args.extcap_interface is None:
        extcap_interfaces()
        sys.exit(0)

    if len(unknown) > 1:
        print("Extcap Example %d unknown arguments given" % len(unknown))

    interface = args.extcap_interface

    if args.extcap_config:
        extcap_config(interface, option)
    elif args.extcap_dlts:
        extcap_dlts(interface)
    elif args.capture:
        if args.fifo is None:
            sys.exit(1)
        try:
            extcap_capture(interface, args.fifo, args.channel)
        except KeyboardInterrupt:
            pass
    else:
        usage()
        sys.exit(1)
