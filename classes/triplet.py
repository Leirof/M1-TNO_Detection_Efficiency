from numpy import *
from classes.block import Block

class Triplet():
    __slots__ = ('id','shotList','block','dataPath')
    all = {}

    def __init__(self, id = None, shotList = None, block = None, dataPath = None):
        self.id         :str        = id
        self.shotList   :list       = [] if shotList is None else shotList
        self.block      :Block      = block
        self.dataPath   :str        = dataPath

        if self not in block.tripletList:
            block.tripletList.append(self)

        if id in Triplet.all:
            raise ValueError("A triplet with this ID already exist")
        else:
            Triplet.all.update({self.id:self})

    def unload(self):
        for shot in self.shotList:
            shot.unload()

    def to_dict(self):
        d = {}
        for shot in self.shotList:
            d.update({f"shot {shot.id}":shot.to_dict()})
        return {'id':self.id,'shotList':d}

    def to_ai_ready(self, maxCCD = 36):
        triplet_data = []
        for shot in self.shotList:
            shot_data = shot.to_ai_ready(maxCCD = maxCCD, randomCCD = True)
            triplet_data.append(shot_data)

        return array(triplet_data).reshape(len(shot_data)*len(triplet_data))