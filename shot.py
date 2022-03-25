
class Shot():
    __slots__ = ('id','ccdList','triplet','block','dataPath')

    all = {}

    def __init__(self, id, ccdList = None, triplet = None, block = None, dataPath = None):
        self.id = id
        self.ccdList = [] if ccdList is None else ccdList
        self.triplet = triplet
        self.block = block
        self.dataPath = dataPath
        if id in Shot.all: raise ValueError("A shot with this ID already exist")
        Shot.all.update({self.id:self})

    def unload(self):
        for ccd in self.ccdList:
            ccd.unload()

    def to_dict(self):
        d = {}
        for ccd in self.ccdList:
            d.update({f"ccd {ccd.id}":ccd.to_dict()})
        return {'id':self.id,'ccdList':d}