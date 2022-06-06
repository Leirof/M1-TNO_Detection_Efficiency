from block import Block
class Triplet():
    __slots__ = ('id','shotList','block','dataPath')

    all = {}

    def __init__(self, id = None, shotList = None, block = None, dataPath = None):
        self.id = id
        self.shotList = [] if shotList is None else shotList
        self.block = block
        block.tripletList.append(self)
        self.dataPath = dataPath
        if id in Triplet.all: raise ValueError("A triplet with this ID already exist")
        Triplet.all.update({self.id:self})

    def unload(self):
        for shot in self.shotList:
            shot.unload()

    def to_dict(self):
        d = {}
        for shot in self.shotList:
            d.update({f"shot {shot.id}":shot.to_dict()})
        return {'id':self.id,'shotList':d}