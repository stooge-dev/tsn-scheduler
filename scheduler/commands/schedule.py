from ..file import  read_network_from_csv, read_streams_from_csv
from ..specific import GracuniasScheduler

"""
PUBLIC SERVICE ANNOUNCMENT: all times are in microsecond
"""

def schedule_command(args):
    # TODO: queues for every device are the same currently 
    scheduled_queues = args.scheduled_queues
    total_queues = args.total_queues
    best_effort_queues = total_queues - scheduled_queues

    network = read_network_from_csv(args.network_filename)
    streams = read_streams_from_csv(args.streams_filename, network)

    if args.method == "graciunas":
        scheduler = GracuniasScheduler(network, scheduled_queues)
        offsets = scheduler.schedule(streams)
        for offset in offsets:
            print(offset.stream_name)
            print(offset.frame_idx)
            print(offset.value)

        if args.save_offset_file != None:
            pass
            # TODO: save

    elif args.method == "hermes":
        pass

# TODO: generate GCL out of model
# TODO: visualize the GCL?