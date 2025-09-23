class Node():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        return self.name == other.name