from numpy import *
from classes.block import Block
from classes.triplet import Triplet

class Shot():
    __slots__ = ('id','ccdList','triplet','block','dataPath')
    all = {}

    def __init__(self, id, ccdList = None, triplet = None, block = None, dataPath = None):
        self.id         :str        = id
        self.ccdList    :list       = [] if ccdList is None else ccdList
        self.triplet    :Triplet    = triplet
        self.block      :Block      = block
        self.dataPath   :str        = dataPath

        if self not in triplet.shotList:
            triplet.shotList.append(self)

        if id in Shot.all:
            raise ValueError("A shot with this ID already exist")
        else:
            Shot.all.update({self.id:self})

    def unload(self):
        for ccd in self.ccdList:
            ccd.unload()

    def to_dict(self):
        d = {}
        for ccd in self.ccdList:
            d.update({f"ccd {ccd.id}":ccd.to_dict()})
        return {'id':self.id,'ccdList':d}

    def to_ai_ready(self, maxCCD = 36, randomCCD = True, **kwargs):
        shot_data = []
        already_selected = []
        for i in range(maxCCD):

            if randomCCD:
                r = random.randint(0,len(self.ccdList))
                while r in already_selected:
                    r = random.randint(0,len(self.ccdList))
            else: r = i

            ccd_data = self.ccdList[r].to_ai_ready()
            shot_data.append(ccd_data)
        return array(shot_data).reshape(len(shot_data)*len(ccd_data))