from typing import Sequence

from .network import Link

class Stream():
    def __init__(self, name: str, length: int, path: Sequence[Link], deadline: int, period: int):
        self.name = name
        self.length = length
        self.path = path
        self.deadline = deadline
        self.period = period

    def dst(self):
        return self.path[len(self.path) - 1]
    
    def src(self):
        return self.path[0]
    
    def adjacent_link_pairs(self):
        alp = []
        for link1 in self.path:
            for link2 in self.path:
                if link1.dst == link2.src and [link1, link2] not in alp:
                    alp.append((link1, link2))
                else:
                    continue

        return alp
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return "Stream(" + self.name + ")"