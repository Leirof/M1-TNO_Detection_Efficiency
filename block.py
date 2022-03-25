
class Block():
    __slots__ = ('id','tripletList','dataPath')
    
    all = {}

    def __init__(self, id, tripletList=None, dataPath = None):
        self.id = id
        self.tripletList = [] if tripletList is None else tripletList
        self.dataPath = dataPath
        if id in Block.all: raise ValueError("A block with this ID already exist")
        Block.all.update({self.id:self})

    def unload(self):
        for triplet in self.tripletList:
            triplet.unload()

    def to_dict(self):
        d = {}
        for triplet in self.tripletList:
            d.update({f"triplet {triplet.id}":triplet.to_dict()})
        return {'id':self.id,'tripletList':d}