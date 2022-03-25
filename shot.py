
class Shot():
    __slots__ = ('__dict__','id','ccdList','triplet','block','dataPath')

    all = {}

    def __init__(self, id, ccdList = [], triplet = None, block = None, dataPath = None):
        self.id = id
        self.ccdList = ccdList
        self.triplet = triplet
        self.block = block
        self.dataPath = dataPath
        if id in Shot.all: raise ValueError("A shot with this ID already exist")
        Shot.all.update({self.id:self})