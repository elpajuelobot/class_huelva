# Importar Pandas
import pandas as pd

#TODO Abrir el archivo .csv
df = pd.read_csv("spells.csv", on_bad_lines='skip')

#TODO Mostrar lista completa
print("=" * 50, "\nTabla de Hechizos:\n", "=" * 50)
print("Total de hechizos:", len(df))

print("=" * 50)
print("Hechizos en menú principal:", df.head(6))

open_menu = input("\n\n¿Abrir libro de hechizos?\n")

if "sí" in open_menu or "si" in open_menu:
    print(f"\n\n{df.to_string(index=False)}")
else:
    print("ok")
