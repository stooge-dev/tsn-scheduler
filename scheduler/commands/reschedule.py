from ..file import  read_network_from_csv, read_streams_from_csv, write_offsets_to_file, read_offsets_from_file
from ..specific import GracuniasScheduler

def reschedule_command(args):
    # TODO: queues for every device are the same currently 
    scheduled_queues = args.scheduled_queues
    total_queues = args.total_queues
    best_effort_queues = total_queues - scheduled_queues

    network = read_network_from_csv(args.network_filename)
    streams = read_streams_from_csv(args.streams_filename, network)

    if args.method == "graciunas":
        pre_offsets = None
        if args.load_offset_file != None:
            pre_offsets = read_offsets_from_file(args.load_offset_file, network)

        new_streams = None
        if args.new_streams_filename != None:
            new_streams = read_streams_from_csv(args.new_streams_filename, network)

        # TODO: give pre_offsets to scheduler
        scheduler = GracuniasScheduler(network, scheduled_queues)
        offsets = scheduler.schedule(streams, pre_offsets, new_streams)

        if offsets == None:
            print("[-] No offsets scheduled")
        elif args.save_offset_file != None:
            write_offsets_to_file(args.save_offset_file, offsets)

    elif args.method == "hermes":
        pass