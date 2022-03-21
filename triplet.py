
class Triplet():

    all = []
    count = 0
    lastUsedID = 0

    def __init__(self, num = None, shotList = []):
        self.id = Triplet.lastUsedID
        Triplet.lastUsedID += 1
        self.num = num
        self.shotList = shotList