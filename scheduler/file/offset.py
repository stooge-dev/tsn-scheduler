from typing import Sequence

from ..business import Offset, Link, Node

import csv

def write_offsets_to_file(filename: str, offsets: Sequence[Offset]):
    with open(filename, "x") as csvfile:
        fieldnames = ['stream_name', 'frame_idx', 'value', 'link']
        offsets_writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)

        offsets_writer.writeheader()

        for offset in offsets:
            link = offset.link.src + ":" + offset.link.dst
            stream_dict = {'stream_name': offset.stream_name, 'frame_idx': offset.frame_idx, 'value': offset.value, 'link': link}
            offsets_writer.writerow(stream_dict)

def read_offsets_from_file(filename: str, network) -> Sequence[Offset]:
    with open(filename) as csvfile:
        offsets_reader = csv.DictReader(csvfile)

        offsets = []
        for offset_row in offsets_reader:
            path_nodes_separator = ":"
            path_nodes = offset_row["link"].split(path_nodes_separator)
            idx_link = network.links.index(Link(Node(path_nodes[0]), Node(path_nodes[1]), 1,1,1))
            
            offset = Offset(stream_name=offset_row["stream_name"], 
                            frame_idx=int(offset_row["frame_idx"]), 
                            value=int(offset_row["value"]), 
                            link=network.links[idx_link])
            offsets.append(offset)

        return offsets