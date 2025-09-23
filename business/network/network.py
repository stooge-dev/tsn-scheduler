from typing import Sequence

from .link import Link



class Network():
    def __init__(self, links: Sequence[Link]):
        self.links = links

    def __repr__(self):
        repr = "Network(["
        for link in self.links:
            repr = repr + link.__str__() + ", "

        repr = repr + "])"

        return repr
    