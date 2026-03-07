import matplotlib.pyplot as plt
import pandas as pd
import sys

try:
    # Cargar CSV
    df = pd.read_csv('spells.csv')

    # Calcular el Daño Base a través de Elemento
    element_destroy = df.groupby('Elemento')['Daño_Base'].mean().sort_values(ascending=False)

    # Creación del gráfico
    fig, ax = plt.subplots()

    # Elección de tipo de gráfico(Barra) // Asignar color a cada barra
    element_destroy.plot(kind='bar', color=['#e74c3c', '#3498db', '#2ecc71', '#f1c40f', '#95a5a6'])

    # Título del gráfico
    ax.set_title('Promedio daño base por Elemento')
    # Título para coordenada Y
    ax.set_ylabel('Daño promedio')
    # Título para coordenada X
    ax.set_xlabel("Elemento")
    # Rotar los nombres para una mejor lectura
    ax.tick_params(axis='x', rotation=0) # ! Esta línea ha sido creada por Gemini porque los nombres se veían al revés

    # Mostrar gráfico final
    plt.show()
except KeyboardInterrupt:
    print("Adios")
    sys.exit()
