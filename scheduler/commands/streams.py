from ..utils import write_streams_to_csv, read_network_from_csv, generate_streams

def streams_command(args):
    network = read_network_from_csv(args.network_filename)
    streams = generate_streams(args.count, network, args.seed)
    write_streams_to_csv(args.save_to, streams)