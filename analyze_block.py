import yaml

def analyze(file):
    data = yaml.safe_load(open(file))
    for             block_key,      block_value     in block.items():
        for         triplet_key,    triplet_value   in block_value["tripletList"].items():
            for     shot_key,       shot_value      in triplet_value["shotList"].items():
                for ccd_key,        ccd_value       in shot_value["ccdList"].items():
