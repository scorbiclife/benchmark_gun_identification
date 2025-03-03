import os
import os.path

import lifelib

def load_guns(guns_directory):
    guns = {}
    for filename in os.listdir(guns_directory):
        try:
            if not filename.endswith(".rle"):
                continue
            with open(os.path.join(guns_directory, filename), mode="r", encoding="utf-8") as f:
                filecontent = f.read()
                guns[filename] = filecontent
        except UnicodeDecodeError as error:
            print(filename, error)
    print(f"{len(guns)} guns loaded")
    return guns

def run_idgun(guns, identify_gun):
    lt4 = lifelib.load_rules("b3s23").lifetree(n_layers=4)
    gun_bounding_boxes = {}
    for gun_name in sorted(list(guns.keys())):
        results = identify_gun(guns[gun_name], lt4)
        if results is not None:
            # should update gun
            if len(results) == 1:
                (gun_category, bounding_box_size, pattern), = results
                # print(gun_name, gun_category, lt4.pattern(pattern).getrect())
            # should update gun and guntrue
            elif len(results) == 2:
                (gun_category, bounding_box_size, pattern), (guntrue_category, _, _) = results
                # print(gun_name, gun_category, lt4.pattern(pattern).getrect())
