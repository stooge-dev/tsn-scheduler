#!/bin/usr/env python3

import argparse

def parse_args():
    parser = argparse.ArgumentParser(prog="tsnscheduler", description="Schedules frames for streams for the given network")

    """
    Argument needs a file which contains the following content:
    src,dst,speed,delay,marcotick
    ...

    src meaning the source node of the link
    dst meaning the destination node of the link
    speed the speed in MBs of the link
    delay the e.g. propagation or processing delay of the link (in ) TODO: unit missing
    marcotick the time granularity of the physical link (in ) TODO: unit missing
    """
    parser.add_argument("-nf", "--network_filename", action="store", required=True, help="Filename of network csv")

    parser.add_argument("-sf", "--streams_filename", action="store", required=True, help="Filename of stream csv")

    parser.add_argument("-sq", "--scheduled_queues", action="store", required=False, default=7)
    parser.add_argument("-tq", "--total_queues", required=False, default=8)

    # parser.add_argument("period", action="store", help="Period duration of streams")

    return parser.parse_args()


