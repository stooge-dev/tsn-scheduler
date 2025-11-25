from .node import Node

class Link():
    def __init__(self, src: Node, dst: Node, mega_bits_per_second: int, delay: int, macrotick: int):
        self.src = src
        self.dst = dst
        self.mega_bits_per_second = mega_bits_per_second
        self.bits_per_second = mega_bits_per_second * 1000 * 1000
        self.bits_per_microsecond = mega_bits_per_second
        self.bytes_per_microsecond = mega_bits_per_second / 8
        self.delay = delay
        self.macrotick = macrotick

        self.bytes_per_second = self.bits_per_second / 8

    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst
    
    def __repr__(self):
        return self.src.__repr__() + " to " + self.dst.__repr__()
    
    def __str__(self):
        return "Link(" + self.src.__repr__() + "-" + self.dst.__repr__() + ")"
    
    def __hash__(self):
        return hash(self.__repr__())