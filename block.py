
class Block():
    __slots__ = ('__dict__','id','triplets','orphanShots','dataPath')
    
    all = {}

    def __init__(self, id, triplets=[], orphanShots = [],dataPath = None):
        self.id = id
        self.triplets = triplets
        self.orphanShots = orphanShots
        self.dataPath = dataPath
        if id in Block.all: raise ValueError("A block with this ID already exist")
        Block.all.update({self.id:self})

