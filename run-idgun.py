import os

from catagolue.initialise.idgun import identify_gun

guns = []
for filename in os.listdir("./glider_guns/fixed"):
    try:
        with open("./glider_guns/fixed/" + filename, mode="r", encoding="utf-8") as f:
            filecontent = f.read()
            guns.append(filecontent)
    except UnicodeDecodeError as error:
        print(filename, error)
