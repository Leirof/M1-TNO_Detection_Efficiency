from numpy import *
from copy import *
import os
import yaml

N = 100 # number of subset per blocks

for file in os.listdir("data/"):
    if os.path.isdir("data/" + file): continue
    if not file.endswith("properties.yml"): continue
    
    path = "data/" + file.replace("properties.yml","subsets")
    if not os.path.isdir(path):
        os.makedirs(path)

    existing = len(os.listdir(path))

    number_of_ccd = random.randint(15,30)
    cpt = existing
    for i in range(N - existing):
        subset = zeros(40).astype(bool)
        while sum(subset) < number_of_ccd:
            subset[random.randint(0,36)] = True
        
        block = yaml.safe_load(open(os.path.join("data",file)))

        new_subset = deepcopy(block)

        for             block_key,      block_value     in block.items():
            for         triplet_key,    triplet_value   in block_value["tripletList"].items():
                for     shot_key,       shot_value      in triplet_value["shotList"].items():
                    for ccd_key,        ccd_value       in shot_value["ccdList"].items():
                        
                        if not subset[int(ccd_value["id"])]:
                            new_subset[block_key]["tripletList"][triplet_key]["shotList"][shot_key]["ccdList"].pop(ccd_key)
                        
                        try:
                            if int(ccd_value["id"]) > 35:
                                new_subset[block_key]["tripletList"][triplet_key]["shotList"][shot_key]["ccdList"].pop(ccd_key)
                        except: pass

        new_file = os.path.join(path,file.replace("properties.yml","subset_") + array2string(subset.astype(int), separator="")[1:-1] + ".yml")
        yaml.dump(new_subset, open(new_file,"w"))
        cpt = existing + i + 1
        print(cpt, new_file)
        


