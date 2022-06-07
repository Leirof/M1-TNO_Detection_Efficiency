from numpy import *

class Block():
    __slots__ = ('id','tripletList','dataPath', 'rates')
    
    all = {}

    def __init__(self, id, tripletList=None, rates=None, dataPath = None):
        self.id             :str            = id
        self.tripletList    :list           = [] if tripletList is None else tripletList
        self.rates          :list           = [] if rates       is None else rates
        self.dataPath       :str            = dataPath

        if id in Block.all:
            raise ValueError("A block with this ID already exist")
        else:
            Block.all.update({self.id:self})

    def unload(self):
        for triplet in self.tripletList:
            triplet.unload()

    def to_dict(self):
        t = {}
        r = {}
        for triplet in self.tripletList:
            t.update({f"triplet {triplet.id}":triplet.to_dict()})
        for rate in self.rates:
            r.update({f"rate_{round(rate.min_vel,1)}-{round(rate.max_vel,1)}":rate.to_dict()})
        return {'id':self.id,'rates':r,'tripletList':t}

    def to_ai_ready(self, func, vel, maxTriplet, maxCCD, randomTriplet = True, randomCCD = True):
        block_data = []
        already_selected = []
        rate_data = None
        for i in range(maxTriplet):

            if randomTriplet:
                r = random.randint(0,len(self.tripletList))
                while r in already_selected:
                    r = random.randint(0,len(self.tripletList))
            else: r = i

            triplet_data = self.tripletList[r].to_ai_ready(maxCCD)
            block_data.append(triplet_data)

        block_data = array(block_data).reshape(len(block_data)*len(triplet_data))

        # Check if the desired detection rate was already measured for this block
        for rate in self.rates:
            if rate.min_vel <= vel and vel <= rate.max_vel and rate.func == func:
                rate_data = rate.to_ai_ready()
                break

        if rate_data is None:
            print(self.id)
            return None
        else:
            return concatenate((block_data,rate_data))

        