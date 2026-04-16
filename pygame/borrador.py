import json

with open("src\\data\\json\\animals_path.json", "r", encoding="utf-8") as data:
    paths = json.load(data)


print(paths["stag"])
