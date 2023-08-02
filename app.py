import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def cargar_datos(archivo):
    return pd.read_csv(archivo)

def grafico_distribucion_siniestros_por_hora(data):
    data['hora'] = pd.to_datetime(data['hora'])
    data['hora_del_dia'] = data['hora'].dt.hour
    siniestros_por_hora = data['hora_del_dia'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(siniestros_por_hora.index, siniestros_por_hora.values)
    plt.xlabel('Hora del día')
    plt.ylabel('Cantidad de siniestros')
    plt.title('Distribución de siniestros viales por hora del día')
    plt.xticks(range(24))
    plt.grid(axis='y')

    # Crear el componente de Matplotlib para Tkinter
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().pack_forget()
    root.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=TOP, padx=10, pady=10)

def grafico_tasa_supervivencia(data):
    homicidios = data[data['causa'] == 'homicidio']['cantidad_victimas'].sum()
    lesiones = data[data['causa'] == 'lesiones']['cantidad_victimas'].sum()
    tasa_supervivencia = lesiones / (homicidios + lesiones) * 100

    plt.figure(figsize=(8, 6))
    plt.pie([lesiones, homicidios], labels=['Supervivencia', 'Fallecimiento'], colors=['green', 'red'], autopct='%1.1f%%')
    plt.title('Tasa de Supervivencia después de un siniestro vial')

    # Crear el componente de Matplotlib para Tkinter
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().pack_forget()
    root.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=TOP, padx=10, pady=10)

    print(f"Tasa de supervivencia después de un siniestro: {tasa_supervivencia:.2f}%")

def ejecutar_funcion():
    seleccion = combo.get()
    data = cargar_datos('victimas.csv')

    if seleccion == 'Gráfico de distribución de siniestros por hora':
        grafico_distribucion_siniestros_por_hora(data)
    elif seleccion == 'Gráfico de tasa de supervivencia':
        grafico_tasa_supervivencia(data)

# Crear la ventana de la aplicación
root = Tk()
root.title("Aplicación de Ciencia de Datos")
root.geometry('800x600')  # Establecer tamaño máximo de la ventana

# Crear un Combobox para seleccionar la función
opciones = ['Gráfico de distribución de siniestros por hora', 'Gráfico de tasa de supervivencia']
combo = ttk.Combobox(root, values=opciones)
combo.pack(pady=10)

# Crear un botón para ejecutar la función seleccionada
boton_ejecutar = Button(root, text="Ejecutar", command=ejecutar_funcion)
boton_ejecutar.pack(pady=5)

root.mainloop()