import sys

from run_idgun import run_idgun, load_guns
import old_idgun
import new_idgun

gun_path = sys.argv[2] if len(sys.argv) >= 2 else "./more_glider_guns/gun"
gun_dataset = load_guns(gun_path)

try:
    if sys.argv[1] == "old":
        run_idgun(gun_dataset, old_idgun.identify_gun)
    elif sys.argv[1] == "new":
        run_idgun(gun_dataset, new_idgun.identify_gun)
    else: 
        raise IndexError()
except IndexError:
    print("usage: python3 run-idgun.py (old|new)", file=sys.stderr)

