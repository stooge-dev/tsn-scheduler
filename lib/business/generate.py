import random

from scheduler.business import Network, Stream
from scheduler.constants import MAX_MTU_SIZE_IN_BYTES

from typing import Sequence

def get_first_link_with_src_endsystem(network):
    first_link_idx = random.randrange(0, len(network.links) - 1)
    first_link = network.links[first_link_idx]
    
    while(first_link.src.is_switch()):
        first_link_idx = random.randrange(0, len(network.links) - 1)
        first_link = network.links[first_link_idx]

    return first_link

def generate_path(first_link, network):
    # TODO: path should not contain links that go backwards, e.g. E to D, D to E
    path = [first_link]
    current_link = first_link
    random_link_idx = [x for x in range(len(network.links) - 1)]
    random.shuffle(random_link_idx)
    for link_idx in random_link_idx:
        link = network.links[link_idx]

        if link.src == current_link.dst and link not in path and path[0].src != link.dst:
            path.append(link)
            current_link = link

        previous_link_has_endsystem_as_destination = link.dst.is_endsystem()
        if previous_link_has_endsystem_as_destination:
            break    

    return path

def generate_deadline_for_stream(path):
    deadline = 0
    for link in path:
        # heuristic...
        deadline += (MAX_MTU_SIZE_IN_BYTES / link.bytes_per_microsecond + link.delay) # * 0.66

    # hyperperiod heuristic...
    hyperperiod_multiple = random.sample([x*2 for x in range(1, 3)], 1)[0]
    deadline *= int(hyperperiod_multiple)
        
    return deadline

def should_stream_be_discarded(path):
    path_to_short = len(path) < 2
    path_dst_not_endsystem = path[-1].dst.is_switch()
    return path_to_short or path_dst_not_endsystem

def generate_streams(count: int, / , *, network: Network, seed: int) -> Sequence[Stream]:
    random.seed(seed)

    streams = []
    current_idx = 0
    while len(streams) < count:
        
        first_link = get_first_link_with_src_endsystem(network)
        path = generate_path(first_link, network)
        
        if should_stream_be_discarded():
            continue

        deadline = generate_deadline_for_stream(path)

        stream_name = "stream"+str(current_idx)
        # FIXME: make streams with more than one frame
        streams.append(Stream(stream_name, MAX_MTU_SIZE_IN_BYTES, path, int(deadline), int(deadline)))
        current_idx += 1

    return streams