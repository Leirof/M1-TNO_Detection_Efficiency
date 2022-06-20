from numpy import *
from classes.block import Block

class Triplet():
    __slots__ = ('id','shotList','block','dataPath','rates')
    all = {}

    def __init__(self, id = None, shotList = None, block = None, dataPath = None, rates = None):
        self.id         :str        = id
        self.shotList   :list       = [] if shotList is None else shotList
        self.rates      :list       = [] if rates    is None else rates
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
        r = {}
        for shot in self.shotList:
            d.update({f"shot {shot.id}":shot.to_dict()})
        for rate in self.rates:
            min_vel = round(rate.max_vel,1) if rate.min_vel is not None else None
            max_vel = round(rate.min_vel,1) if rate.max_vel is not None else None
            r.update({f"Detection rate using function {rate.func} for velocity {min_vel}-{max_vel}":rate.to_dict()})
        return {'id':self.id,'rates':r,'shotList':d}

    def to_ai_ready(self, withrate = True, func = None, vel = 4.5, maxCCD = 36, randomCCD = True, **kwargs):
        triplet_data = []
        outputs = 0
        for shot in self.shotList:
            shot_data = shot.to_ai_ready(maxCCD = maxCCD, randomCCD = randomCCD)
            triplet_data.append(shot_data)
        triplet_data = array(triplet_data).reshape(len(triplet_data)*len(shot_data))

        if not withrate: return triplet_data, None

        rate_data = None
        for rate in self.rates:
            if vel is None or rate.min_vel is None or rate.max_vel is None or (rate.min_vel <= vel and vel <= rate.max_vel):
                if func is None or rate.func == func:
                    outputs += 4
                    rate_data = rate.to_ai_ready()
                    break

        if rate_data is None:
            return None, None
        else:
            return concatenate((triplet_data,rate_data)), outputs