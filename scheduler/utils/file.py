
from typing import Sequence

from ..business import Network, Node, Stream, Link

import csv

def read_network_from_csv(filename: str) -> Network:
    with open(filename) as csvfile:
        linkreader = csv.DictReader(csvfile)
        
        links = []
        for row in linkreader:
            src = Node(row["src"])
            dst = Node(row["dst"])

            link = Link(src=src, dst=dst,delay=int(row["delay"]),speed=int(row["speed"]),macrotick=int(row["macrotick"]))
            links.append(link)

            link = Link(src=dst, dst=src, delay=int(row["delay"]),speed=int(row["speed"]),macrotick=int(row["macrotick"]))
            links.append(link)
            
        return Network(links)

def read_path(string: str, network: Network) -> Sequence[Node]:
    path_links_separator = ";"
    path_str = string.split(path_links_separator)

    path = []
    for link_str in path_str:
        path_nodes_separator = ":"
        path_nodes = link_str.split(path_nodes_separator)
        idx_link = network.links.index(Link(Node(path_nodes[0]), Node(path_nodes[1]), 1,1,1))
        path.append(network.links[idx_link])

    return path


def read_streams_from_csv(filename: str, network: Network) -> Sequence[Stream]:
    with open(filename) as csvfile:
        streams_reader = csv.DictReader(csvfile)

        streams = []
        for stream_row in streams_reader:
            stream = Stream(stream_row["name"], 
                            int(stream_row["length"]), 
                            read_path(stream_row["path"], network), 
                            int(stream_row["deadline"]), 
                            int(stream_row["period"]))
            streams.append(stream)

        return streams
    
def write_streams_to_csv(filename: str, streams: Sequence[Stream]):
    with open(filename) as csvfile:
        fieldnames = ['name', 'length', 'deadline', 'path', 'period']
        streams_writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)

        for stream in streams:
            # TODO: Path needs to be formated.
            stream_dict = {'name': stream.name, 'length': stream.length, 'deadline': stream.deadline, 'path': stream.path, 'period': stream.period}
            streams_writer.writerow(stream_dict)