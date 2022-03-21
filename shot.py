
class Shot():

    all = []
    count = 0
    lastUsedID = 0

    def __init__(self, ccdList = []):
        self.id = Shot.lastUsedID
        Shot.lastUsedID += 1
        self.ccdList = ccdList