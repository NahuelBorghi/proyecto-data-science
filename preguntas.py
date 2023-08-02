import pandas as pd
import matplotlib.pyplot as plt

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
    plt.savefig('grafico.png')
    plt.show()

def grafico_tasa_supervivencia(data):
    data['hora'] = pd.to_datetime(data['hora'])
    homicidios = data[data['causa'] == 'homicidio']['cantidad_victimas'].sum()
    lesiones = data[data['causa'] == 'lesiones']['cantidad_victimas'].sum()
    tasa_supervivencia = lesiones / (homicidios + lesiones) * 100

    plt.figure(figsize=(8, 6))
    plt.pie([lesiones, homicidios], labels=['Supervivencia', 'Fallecimiento'], colors=['green', 'red'], autopct='%1.1f%%')
    plt.title('Tasa de Supervivencia después de un siniestro vial')
    plt.savefig('grafico.png')
    plt.show()

    print(f"Tasa de supervivencia después de un siniestro: {tasa_supervivencia:.2f}%")

def menu():
    data = cargar_datos('victimas.csv')

    while True:
        print("\n--- Menú ---")
        print("1. Ver gráfico de distribución de siniestros por hora")
        print("2. Ver gráfico de tasa de supervivencia")
        print("0. Salir")
        opcion = input("Ingrese el número de opción que desee: ")

        if opcion == '1':
            grafico_distribucion_siniestros_por_hora(data)
        elif opcion == '2':
            grafico_tasa_supervivencia(data)
        elif opcion == '0':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
