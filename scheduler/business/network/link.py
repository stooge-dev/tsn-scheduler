from .node import Node

class Link():
    def __init__(self, src: Node, dst: Node, speed: int, delay: int, macrotick: int):
        self.src = src
        self.dst = dst
        self.speed = speed
        self.delay = delay
        self.macrotick = macrotick

    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst
    
    def __repr__(self):
        return self.src.__repr__() + "to" + self.dst.__repr__()
    
    def __str__(self):
        return "Link(" + self.src.__repr__() + " - " + self.dst.__repr__() + ")"
    
    def __hash__(self):
        return hash(self.__repr__())