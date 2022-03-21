
class Block():
    
    all = []
    count = 0
    lastUsedID = 0

    def __init__(self):
        self.id = Block.lastUsedID
        Block.lastUsedID += 1

