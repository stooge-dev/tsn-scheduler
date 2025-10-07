import random

from typing import Sequence

from ..business import Stream, Network
from ..constants import MAX_MTU_SIZE_IN_BYTES

def generate_streams(count: int, network: Network) -> Sequence[Stream]:
    # FIXME: generates same streams for same network
    random.seed(1)

    streams = []
    current_idx = 0
    while len(streams) < count:
        first_link_idx = random.randrange(0, len(network.links) - 1)
        first_link = network.links[first_link_idx]

        # TODO: path should not contain links that go backwards, e.g. E to D, D to E
        path = [first_link]
        current_link = first_link
        deadline = 0
        for link in network.links:

            if link.src == current_link.dst and link not in path:
                path.append(link)
                current_link = link

            # heuristic...
            deadline += (MAX_MTU_SIZE_IN_BYTES / link.speed + link.delay) * 0.66
            

        if len(path) < 2:
            continue

        # hyperperiod heuristic...
        hyperperiod_multiple = random.sample([x*2 for x in range(1, 3)], 1)[0]
        deadline *= int(hyperperiod_multiple)

        stream_name = "stream"+str(current_idx)
        # FIXME: make streams with more than one frame
        streams.append(Stream(stream_name, MAX_MTU_SIZE_IN_BYTES, path, int(deadline), int(deadline)))
        current_idx += 1

    return streams

        
