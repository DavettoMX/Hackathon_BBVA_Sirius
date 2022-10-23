"""
IDENTIFICAR USUARIOS MAYORES DE 65 AÑOS
QUE NO TIENEN REGISTROS DE MOVIMIENTOS BANCARIOS
Y QUE NO TIENEN REGISTROS DE TARJETAS DE CRÉDITO
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import obtencion_data as od


class Identificacion:
    def __init__(self):
        self.data = od.BaseDatos()
        self.publico_objetivo = self.data.obtener_publico_objetivo()
        self.movimientos_objetivo = self.data.movimientos_objetivo()
        self.movimientos = self.data.obtener_movimientos()

    def obtener_movimientos(self):
        publico_objetivo = self.publico_objetivo

        # Si el publico objetivo no tiene movimientos bancarios se considera
        # como un usuario objetivo para identificar

        movimientos_objetivo = self.movimientos_objetivo

        objetivos = []
        no_objetivos = []

        for index, movimiento in enumerate(movimientos_objetivo):
            for usuario in movimiento:
                if usuario[0] not in no_objetivos:
                    no_objetivos.append(usuario[0])

        for index, usuarios in enumerate(publico_objetivo):
            if usuarios[0] not in no_objetivos:
                objetivos.append(usuarios)

        return objetivos


if __name__ == '__main__':
    identificacion = Identificacion()
    identificacion.obtener_movimientos()