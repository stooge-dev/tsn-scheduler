#!/bin/bash/env python3

"""
PUBLIC SERVICE ANNOUNCMENT: all times are in microsecond
"""

from .utils import ArgumentParser, read_network_from_csv, read_streams_from_csv, generate_streams
from .specific import GracuniasScheduler

argumentParser = ArgumentParser()
args = argumentParser.parse_arguments()

if args.command == "schedule":
    # TODO: queues for every device are the same currently 
    scheduled_queues = args.scheduled_queues
    total_queues = args.total_queues
    best_effort_queues = total_queues - scheduled_queues

    network = read_network_from_csv(args.network_filename)
    #streams = read_streams_from_csv(args.streams_filename, network)
    stream_count = 15
    streams = generate_streams(stream_count, network, 1)

    if args.method == "graciunas":
        scheduler = GracuniasScheduler(network, scheduled_queues)
        scheduler.schedule(streams)
    elif args.method == "hermes":
        pass

elif args.command == "streams":
    network = read_network_from_csv(args.network_filename)
    streams = generate_streams(args.count, network, args.seed)

    # TODO: save to file
    pass

# TODO: make a benchmark generator?
# TODO: generate GCL out of model
# TODO: visualize the GCL?