from typing import Sequence

from .network import Link

class Stream():
    def __init__(self, name: str, bytes: int, path: Sequence[Link], deadline: int, period: int):
        self.name = name
        self.bytes = bytes
        self.path = path
        self.deadline = deadline
        self.period = period

    def dst(self) -> Link:
        return self.path[len(self.path) - 1]
    
    def src(self) -> Link:
        return self.path[0]
    
    def adjacent_link_pairs(self):
        alp = []
        current_idx = 0
        while current_idx < len(self.path) - 1:
            link1 = self.path[current_idx]
            link2 = self.path[current_idx + 1]

            alp.append((link1, link2))
            current_idx += 1

        return alp
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return "Stream(" + self.name + ")"
    
    def __hash__(self):
        return hash(self.name)
    