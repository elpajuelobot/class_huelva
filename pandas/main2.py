import pandas as pd
import time as t

# cargar el csv
df = pd.read_csv('spells.csv') # df = pd.read_csv('data/spells.csv') si estuviera en la carpeta data
print(" CSV cargado")
print("")
print("")
print("")
t.sleep(3)

# ordenamos  de menor a mayor
df_ordenado = df.sort_values('Costo_Mana')
print(df_ordenado)
print("")
print("")
print("")
t.sleep(3)

# quitar duplicados de cada elemento
df_noduplicado = df_ordenado.drop_duplicates('Elemento')
print(df_noduplicado)
print("")
print("")
print("")
t.sleep(3)

# selecionamos las columnas que queremos
resultado = df_noduplicado[['ID', 'Nombre_Hechizo','Costo_Mana', 'Elemento']]
# print resumen
print(resultado)

# ?   https://docs.google.com/document/d/1MjTfGUNJxUNeZkLTwL5evfjmCGeAdj4yQJu-IsH48DM/edit?usp=sharing
