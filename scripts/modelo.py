"""
MODELO DE MACHINE LEARNING PARA DETECCIÓN DE CLIENTES OBJETIVO
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier

import obtencion_data as od

class Modelo:
    def __init__(self):
        self.data = od.BaseDatos()
        self.publico_objetivo = self.data.obtener_publico_objetivo()
        self.giros_de_interes = self.data.obtener_giros_de_interes()
        self.movimientos = self.data.obtener_movimientos()
        self.movimientos_objetivo = self.data.movimientos_objetivo()

    def defnir_usuarios_objetivo(self):
        # Definir listas de clientes objetivo y no objetivo
        clientes_objetivo = []
        clientes_no_objetivo = []

        # Recorrer movimientos objetivo
        for index, movimiento in enumerate(self.movimientos_objetivo):
            for usuario in movimiento:
                    clientes_objetivo.append(usuario)

        for index, movimiento in enumerate(self.movimientos):
            if movimiento[0] not in clientes_objetivo:
                if movimiento[0] not in clientes_no_objetivo:
                    clientes_no_objetivo.append(movimiento)

        # Crear dataframe de clientes objetivo donde no se repita la información
        df_objetivo = pd.DataFrame(clientes_objetivo, columns=['ID_CLIENTE', 'EDAD', 'ESTADO', 'CODIGO POSTAL', 'SEXO', 'MES TRANSACCION', 'DIA TRANSACCION', 'GIRO', 'SUBGIRO'])

        return df_objetivo

    def modelo(self):
        objetivo = self.defnir_usuarios_objetivo()

        # Crear un modelo de Machine Learning que permita identificar a los
        # potenciales clientes objetivo por medio de los movimientos bancarios.

        # Si un cliente de 65 años o más comienza a realizar movimientos bancarios
        # en el área de salud, más de 3 veces al mes, se considerará como un
        # cliente objetivo.

        modelo = RandomForestClassifier(n_estimators=100)

        # Características de los clientes objetivo
        # - Edad: 65 años o más
        # - Subgiros: self.giros_de_interes = self.data.obtener_giros_de_interes()
        # - Movimientos bancarios: 3 veces o más al mes

        # Entrenar el modelo con los datos de los clientes objetivo
        objetivo = objetivo.groupby('ID_CLIENTE').filter(lambda x: len(x) >= 3) # Filtrar clientes objetivo con más de 3 movimientos al mes

        # Entrenar modelo para que identifique a los clientes objetivo
        modelo.fit(objetivo[['EDAD']], objetivo['ID_CLIENTE'])

        # Predecir si un cliente es objetivo o no
        prediccion = modelo.predict(objetivo[['EDAD']])

        # Mostrar resultados
        print(classification_report(objetivo['ID_CLIENTE'], prediccion))

        # Crear una grafica de barras para mostrar el rango de edad de los clientes objetivo
        plt.figure(figsize=(10, 6))
        sns.countplot(x='EDAD', data=objetivo)
        plt.title('Rango de edad de los clientes objetivo')
        plt.show()


# TEST
if __name__ == '__main__':
    modelo = Modelo()
    modelo.modelo()
