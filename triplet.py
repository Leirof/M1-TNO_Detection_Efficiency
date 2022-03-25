
class Triplet():
    __slots__ = ('__dict__','id','shotList','block','dataPath')

    all = {}

    def __init__(self, id = None, shotList = [], block = None, dataPath = None):
        self.id = id
        self.shotList = shotList
        self.block = block
        self.dataPath = dataPath
        if id in Triplet.all: raise ValueError("A triplet with this ID already exist")
        Triplet.all.update({self.id:self})