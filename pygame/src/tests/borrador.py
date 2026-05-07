import json

with open("src\\data\\json\\animals_path.json", "r", encoding="utf-8") as data:
    animals_paths = json.load(data)

for state in animals_paths["stag"]:
    print(f"\n\nEstado: {state}")
    for direction in animals_paths["stag"][state]:
        datos = animals_paths["stag"][state][direction]

        path = datos[0]
        frames = datos[1]
        print(f"Dirección: {direction}")
        print(f"Ruta de la spritesheet:\n{path}\nNúmero de frames: {frames}")
