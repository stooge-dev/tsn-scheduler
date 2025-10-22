#!/bin/bash/env python3

"""
PUBLIC SERVICE ANNOUNCMENT: all times are in microsecond
"""

from .utils import parse_args, read_network_from_csv, read_streams_from_csv, generate_streams
from .scheduler import Scheduler

args = parse_args()

# TODO: queues for every device are the same currently 
scheduled_queues = args.scheduled_queues
total_queues = args.total_queues
best_effort_queues = total_queues - scheduled_queues

network = read_network_from_csv(args.network_filename)
#streams = read_streams_from_csv(args.streams_filename, network)
stream_count = 15
streams = generate_streams(stream_count, network)

scheduler = Scheduler(network, scheduled_queues)
scheduler.schedule(streams)

# TODO: make a benchmark generator?
# TODO: generate GCL out of model
# TODO: visualize the GCL?