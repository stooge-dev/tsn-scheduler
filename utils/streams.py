import random

from typing import Sequence

from ..business import Stream, Network
from ..constants import MAX_MTU_SIZE_IN_BYTES

def generate_streams(count: int, periods: Sequence[int], network: Network, frame_counts: Sequence[int]) -> Sequence[Stream]:
    # TODO: frame_counts and periods not used, currently
    assert len(periods) == count
    assert len(frame_counts) == count

    # TODO: so generates same streams for same network
    random.seed(1)

    # streams need atleast two links

    # TODO: network model change => include differentation between ES and SW?
    streams = []
    current_idx = 0
    while len(streams) < count:
        first_link_idx = random.randrange(0, len(network.links) - 1)
        first_link = network.links[first_link_idx]

        path = [first_link]
        current_link = first_link
        deadline = 0
        for link in network.links:

            if link.src == current_link.dst and link not in path:
                path.append(link)
                current_link = link

            # heuristic...
            deadline += 1.5 * (MAX_MTU_SIZE_IN_BYTES / link.speed + link.delay)

        if len(path) < 2:
            continue

        stream_name = "stream"+str(current_idx)
        streams.append(Stream(stream_name, MAX_MTU_SIZE_IN_BYTES, path, int(deadline), int(deadline)))
        current_idx += 1

    return streams

        
