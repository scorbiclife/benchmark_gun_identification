import sys

from run_idgun import run_idgun, load_guns
import old_idgun
import new_idgun

guntrue_dataset = load_guns("./more_glider_guns/guntrue")
gun_dataset = load_guns("./more_glider_guns/gun")

try:
    if sys.argv[1] == "old":
        run_idgun(gun_dataset, old_idgun.identify_gun)
    elif sys.argv[1] == "new":
        run_idgun(gun_dataset, new_idgun.identify_gun)
    else: 
        raise IndexError()
except IndexError:
    print("usage: python3 run-idgun.py (old|new)", file=sys.stderr)

