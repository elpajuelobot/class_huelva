import matplotlib.pyplot as plt
import csv

# acumular datos
elementos_data = {}

# abrir csv
with open('spells.csv', mode = 'r', encoding = 'utf-8' ) as archivo:
    lector_csv = csv.reader(archivo)
    next(lector_csv) # siguiente linea

    for fila in lector_csv:
        elemento = fila[2] # la tercera columna del csv es indice 2
        costo = int(fila[4]) # la quinta columna del csv es indice 4 ( hay que pasarlo a numero con int)

        if elemento not in elementos_data:
            elementos_data[elemento] = []
            elementos_data[elemento].append(costo) # elemntos con sus costes de mana en lista

# lista de elementos segun sus claves
nombres_elementos = list(elementos_data.keys())

# promedio de mana
promedios_mana = [sum(valores) / len(valores) for valores in elementos_data.values()]

# colores para barras 
colores_dict = {
    'Fuego': 'tab:red',
    'Hielo': 'tab:cyan',
    'Tierra': 'tab:brown',
    'Aire': 'tab:gray',
    'Agua': 'tab:blue'
}

colores_barras = [colores_dict.get(e, 'black') for e in nombres_elementos]

fig, ax = plt.subplots()

barras = ax.bar(nombres_elementos, promedios_mana , color = colores_barras)
# numero de las barras
ax.bar_label(barras, padding = 3, fmt= '%.1f')

ax.set_ylabel('Costo de Maná')
ax.set_title('Promedio de Maná por Elemento')

plt.show()