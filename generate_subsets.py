from numpy import *
import os
import yaml

subset = zeros(36).astype(bool)


for file in os.listdir("data/"):
    if not os.path.isdir("data/" + file.replace(".yml","")):
        os.makedirs("data/" + file.replace(".yml",""))
    for i in range(100):
        while sum(subset) < 18:
            subset[random.randint(0,36)] = True
        
        block = yaml.load(open(os.path.join("data",file)))


        
        break
    break
        

print(subset)