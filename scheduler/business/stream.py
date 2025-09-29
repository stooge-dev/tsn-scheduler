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
    
from abc import ABC, abstractmethod

class StreamDependencyGraph(ABC):
    def __init__(self, streams: Sequence[Stream]):
        self.streams = streams
        self.graph = {}
        self.calculate_dependencies()

    @abstractmethod
    def calculate_dependencies(self):
        pass

class SameLinkSchedulingStreamDependencyGraph(StreamDependencyGraph):
    def calculate_dependencies(self):
        for stream1 in self.streams:
            for stream2 in self.streams:
                if stream1 == stream2:
                    continue

                weight = 0
                for link1 in stream1.path:
                    for link2 in stream2.path:
                        if link1 != link2:
                            continue

                        weight += 1

                self.graph[stream1][stream2] = weight
                self.graph[stream2][stream1] = weight
