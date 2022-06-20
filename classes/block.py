from numpy import *
import json
import os

class Block(): 
    __slots__ = ('id','tripletList','dataPath', 'rates')
    
    all = {}

    def __init__(self, id, tripletList=None, rates=None, dataPath = None):
        self.id             :str            = id
        self.tripletList    :list           = [] if tripletList is None else tripletList
        self.rates          :list           = [] if rates       is None else rates
        self.dataPath       :str            = dataPath

        if id in Block.all:
            raise ValueError(f"A block with the ID {id} already exist")
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
            min_vel = round(rate.max_vel,1) if rate.min_vel is not None else None
            max_vel = round(rate.min_vel,1) if rate.max_vel is not None else None
            r.update({f"Detection rate using function {rate.func} for velocity {min_vel}-{max_vel}":rate.to_dict()})
        return {'id':self.id,'rates':r,'tripletList':t}

    def save(self, folder = "./data", indent = None):
        if not os.path.exists(folder): os.makedirs(folder)
        with open(os.path.join(folder,f'{self.id}.json'), 'w') as fp:
            json.dump({f"block {self.id}": self.to_dict()}, fp, indent=indent)

    def to_ai_ready(self, func = None, vel = 4.5, maxTriplet = 8, maxCCD = 36, randomTriplet = True, randomCCD = True, **kwargs):
        block_data = []
        already_selected = []
        rate_data = None
        outputs = 0
        for i in range(maxTriplet):

            if randomTriplet:
                r = random.randint(0,len(self.tripletList))
                while r in already_selected:
                    r = random.randint(0,len(self.tripletList))
            else: r = i

            triplet_data, _ = self.tripletList[r].to_ai_ready(withrate = False, func = func, vel = vel, maxCCD = maxCCD, randomCCD = randomCCD)
            block_data.append(triplet_data)

        block_data = array(block_data)
        try: block_data = block_data.reshape(len(block_data)*len(triplet_data))
        except:
            print(self.id)
            print(block_data.shape)
            print(type(block_data))
            raise
        

        # Check if the desired detection rate was already measured for this block
        for rate in self.rates:
            if vel is None or rate.min_vel is None or rate.max_vel is None or (rate.min_vel <= vel and vel <= rate.max_vel):
                if func is None or rate.func == func:
                    rate_data = rate.to_ai_ready()
                    outputs += 4

        if rate_data is None:
            return None, None
        else:
            try: return concatenate((block_data,rate_data)), outputs
            except:
                print(self.id)
                print(block_data.shape)
                print(rate_data.shape)
                raise

        