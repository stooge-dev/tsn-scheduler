from scheduler.business import Network, Node,  Link

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