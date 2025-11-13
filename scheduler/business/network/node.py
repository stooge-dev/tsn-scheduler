from enum import StrEnum

class NodeType(StrEnum):
    ES="End System",
    SW="Switch"

class Node():
    def __init__(self, name, type: NodeType):
        self.name = name
        self.type = type

    def __init__(self, string: str):
        split_string = string.split(";")
        self.name = split_string[0]
        self.type = NodeType[split_string[1]]  

    def __repr__(self):
        return self.name + ";" + self.type.value
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        return self.name == other.name and self.type == other.type