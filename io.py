import yaml

def yml_to_objects(file)
    data = yaml.safe_load(open(file))
    for             block_key,      block_value     in data.items():
        block = Block(id="")
        for         triplet_key,    triplet_value   in block_value["tripletList"].items():
            for     shot_key,       shot_value      in triplet_value["shotList"].items():
                for ccd_key,        ccd_value       in shot_value["ccdList"].items():
                    yield block_key, triplet_key, shot_key, ccd_key, ccd_value