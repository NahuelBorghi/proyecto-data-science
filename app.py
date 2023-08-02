import pandas as pd
import numpy as np
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

def grafico_choques_x_anio(data):
    conteo_año = data['periodo'].value_counts()

    #Armo el grafico. Me lo hizo el ChatGPT. No me quedó bien, me genera fracciones entre año y año

    plt.figure(figsize=(8, 6))  
    plt.bar(conteo_año.index, conteo_año)
    plt.xlabel('Año')
    plt.ylabel('Cantidad') 
    plt.title('¿En que año ocurrieron mas choques en la ciudad de Buenos Aires?')
    
    # Crear el componente de Matplotlib para Tkinter
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().pack_forget()
    root.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=TOP, padx=10, pady=10)

def grafico_linea_tiempo_x_periodo_mes(data):
    #Armo un nuevo dataframe con las dos columnas para preparar la linea de tiempo
    df_temporal = data.loc[:, ['mes', 'periodo']]
    #Les saco los nulls, no estoy seguro de que funcione
    df_temporal.fillna(0)
    df_temporal.isnull().sum()
    #Armo un nuevo dataframe con el resultado de los conteos
    df_comparacion = df_temporal.value_counts().reset_index(name='count')
    #Ordeno los resultados primero por periodo y despues por mes
    df_comparacion_ordenada = df_comparacion.sort_values(by=['periodo', 'mes'])
    #Cambio el valor de mes de float a int para poder usar datetime
    df_comparacion_ordenada['mes'] = df_comparacion_ordenada["mes"].astype(int)
    #Creo una columna fecha pasando a datetime la colummna periodo y la columna mes
    df_comparacion_ordenada["fecha"] = df_comparacion_ordenada.apply(lambda x: pd.to_datetime(f"{x['periodo']}-{x['mes']}"), axis=1)
    plt.figure(figsize=(10, 5))
    plt.plot(df_comparacion_ordenada["fecha"], df_comparacion_ordenada["count"], marker='o', linestyle='-', color='b')
    plt.xlabel("Fecha")
    plt.ylabel("Conteo")
    plt.title("grafico de línea de tiempo")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    # Crear el componente de Matplotlib para Tkinter
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().pack_forget()
    root.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=TOP, padx=10, pady=10)

def grafico_barras_choques_mes(data):
    mapeo_meses = {
        1.0: 'Enero',
        2.0: 'Febrero',
        3.0: 'Marzo',
        4.0: 'Abril',
        5.0: 'Mayo',
        6.0: 'Junio',
        7.0: 'Julio',
        8.0: 'Agosto',
        9.0: 'Septiembre',
        10.0: 'Octubre',
        11.0: 'Noviembre',
        12.0: 'Diciembre'
    }

    data['mes_convertido'] = data['mes'].replace(mapeo_meses)

    #Armo un dataframe con el conteo de valores de cada mes

    conteo_mes = data['mes_convertido'].value_counts()

    #Armo el grafico. Me lo hizo el ChatGPT

    plt.figure(figsize=(8, 6))  
    plt.barh(conteo_mes.index, conteo_mes) # eje y / eje x
    plt.gca().invert_yaxis()
    plt.xlabel('Cantidad')
    plt.ylabel('Meses') 
    plt.title('¿En que meses ocurren mas choques en la ciudad de Buenos Aires?')
    
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().pack_forget()
    root.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=TOP, padx=10, pady=10)

def grafico_comparativo_periodo_y_mes(data):
    df_temporal = data.loc[:, ['mes', 'periodo']]
    df_comparacion = df_temporal.value_counts().reset_index(name='count')
    df_comparacion_ordenada = df_comparacion.sort_values(by=['periodo', 'mes'])
    df_comparacion_ordenada['mes'] = df_comparacion_ordenada["mes"].astype(int)
    x = df_comparacion_ordenada['mes'].unique().astype(int) #meses
    
    y1 = df_comparacion_ordenada[(df_comparacion_ordenada['periodo'] == 2015)]['count']
    y2 = df_comparacion_ordenada[(df_comparacion_ordenada['periodo'] == 2016)]['count']
    y3 = df_comparacion_ordenada[(df_comparacion_ordenada['periodo'] == 2017)]['count']

    # Al estar incompleto, es necesario llenar los datos faltantes con un minimo inventado para que no nos achique el gráfico

    y4 = df_comparacion_ordenada[(df_comparacion_ordenada['periodo'] == 2018)]['count']
    y4_filled = np.full_like(x, 600)
    y4_filled[:len(y4)] = y4

    # Código de la linea de tiempo

    plt.plot(x, y1, label='2015')
    plt.plot(x, y2, '-.', label='2016')
    plt.plot(x, y3, '--', label='2017')
    plt.plot(x, y4_filled, ':', label='2018')

    plt.xlabel("X-axis data")
    plt.ylabel("Y-axis data")
    plt.title('Cantidad de choques por mes durante los años 2015-1018')
    plt.legend()
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().pack_forget()
    root.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=TOP, padx=10, pady=10)

def tiposDeChoques(data):
    # Aca busco cuales fueron la cantidad de choques multiples en cada lugar

    choquesMultiples = data[data['tipo_colision1'] == 'multiple']
    choquesMultiplesAutopista = data[(data['tipo_colision1'] == 'multiple') & (data['tipo_calle'] == 'autopista')]


    labels = 'Moto-Auto', 'auto-peaton', 'auto-auto', 'multiple','moto-peaton', 'bici-auto', 'moto-moto', 'otros'
    sizes = [35,17.7,20,13,4.5,4.3,2,3.5]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')

    print(data['tipo_colision1'].value_counts())

    print(f"Los choques multiples en los años mencionados fueron {len(choquesMultiples)} de los cuales {len(choquesMultiplesAutopista)} fueron en autopistas")
    print(f"En el grafico de torta queda representado como 'otros' los accidentes que son casos aislados. Un ejemplo de esto seria accidentes de motos contra traccion a sangre.")

    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().pack_forget()
    root.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=TOP, padx=10, pady=10)

def cantidadChoquesPorUbicacion(data):
    #Primero identifico la cantidad de choques que hubo en general y luego en cada tipo de calle
    cantidadChoques = data['tipo_calle'].value_counts()
    print(cantidadChoques)
    # Aca preparo los datos para presentarlos en un pie chart con los respectivos porcentajes de cada lugar
    plt.figure(figsize=(8, 6)) 
    plt.title("Accidentes de transito en Buenos Aires(2015-2018)")
    cantidadChoques.plot(kind='pie', autopct='%1.1f%%')
    
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().pack_forget()
    root.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=TOP, padx=10, pady=10)

def accidentesComunas(data):
    # print(df.info())
    # Identifico la cantidad de comunas y accidentes en cada una
    totalComunas = data['comuna']
    accidentesPorComuna = totalComunas.value_counts()
    print(accidentesPorComuna)
    # Una vez encontrada la info la preparo para presentar en un bar graph
    plt.figure(figsize=(8, 6)) 
    plt.xlabel('Comunas')
    plt.ylabel('Cantidad de accidentes') 
    plt.title("Accidentes de transito por comunas de Buenos Aires(2015-2018)")
    accidentesPorComuna.plot(kind='barh').invert_yaxis()
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().pack_forget()
    root.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=TOP, padx=10, pady=10)


# Conclusiones

# Hay algun genero predominante entre las victimas?
def genero_victimas(data):
    print(f'{data["sexo"].value_counts()}')


# Cual es el participante acusado mas frecuente?
def acusado_frecuente(data):
    print(f'{data["rol"].value_counts()}')
    print(f'{data["participantes_victimas"].value_counts()}')
    print(f'{data["participantes_acusados"].value_counts()}')


def ejecutar_funcion():
    seleccion = combo_grafico.get()
    seleccion_conclusion = combo_conclusion.get()
    data = cargar_datos('victimas.csv')
    if seleccion == 'distribución de siniestros por hora' and seleccion_conclusion == '':
        grafico_distribucion_siniestros_por_hora(data)
    elif seleccion == 'tasa de supervivencia' and seleccion_conclusion == '':
        grafico_tasa_supervivencia(data)
    elif seleccion == 'choques por mes' and seleccion_conclusion == '':
        grafico_barras_choques_mes(data)
    elif seleccion == 'choques por año' and seleccion_conclusion == '':
        grafico_choques_x_anio(data)
    elif seleccion == 'linea de tiempo por periodo y mes' and seleccion_conclusion == '':
        grafico_linea_tiempo_x_periodo_mes(data)
    elif seleccion == 'comparativo por periodo y mes' and seleccion_conclusion == '':
        grafico_comparativo_periodo_y_mes(data)
    elif seleccion == 'tipos de choques' and seleccion_conclusion == '':
        tiposDeChoques(data)
    elif seleccion == 'choques por tipo de calle' and seleccion_conclusion == '':
        cantidadChoquesPorUbicacion(data)
    elif seleccion == 'siniestros por comuna' and seleccion_conclusion == '':
        accidentesComunas(data)
    
    
    if seleccion_conclusion == 'genero predominante de victimas' and seleccion == '':
        genero_victimas(data)
    elif seleccion_conclusion == 'participante acusado mas frecuente'and seleccion == '':
        acusado_frecuente(data)

# Crear la ventana de la aplicación
root = Tk()
root.title("Aplicación de Ciencia de Datos")
root.geometry('800x600')  # Establecer tamaño máximo de la ventana
notebook = ttk.Notebook(root)
# Crear un Combobox para seleccionar la función
opciones_grafico = [
    '',
    'comparativo por periodo y mes',
    'distribución de siniestros por hora',
    'tasa de supervivencia',
    'choques por mes',
    'choques por año',
    'linea de tiempo por periodo y mes',
    'tipos de choques',
    'choques por tipo de calle',
    'siniestros por comuna'
]
opciones_conclusion = [
    '',
    'genero predominante de victimas',
    'participante acusado mas frecuente'
]

combo_grafico = ttk.Combobox(root, values=opciones_grafico)
combo_grafico.pack(pady=10)
combo_conclusion = ttk.Combobox(root, values=opciones_conclusion)
combo_conclusion.pack(pady=10)

notebook.add(combo_grafico,text="Gráficos", padding=20)
notebook.add(combo_conclusion,text="Conclusiones", padding=20)
notebook.pack()
# Crear un botón para ejecutar la función seleccionada
boton_ejecutar = Button(root, text="Ejecutar", command=ejecutar_funcion)
boton_ejecutar.pack(pady=5)

root.mainloop()