"""
CREACIÓN DE UN MODELO DE MACHINE LEARNING PARA DETECTAR A LOS USUARIOS DE 65 AÑOS O MÁS
Y PREDECIR SI PADECEN DE ALGUNA ENFERMEDAD, POR MEDIO DE LA INFORMACIÓN QUE SE TIENE
DE LOS USUARIOS EN LA BASE DE DATOS Y EN LOS ARCHIVOS CSV.
"""

# Importación de librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
import mysql.connector

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Conexion a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    passwd="adminroot",
    database="hackathon_bbva"
)

connector = mydb.cursor()

# Obtencion de datos
giros_de_interes = connector.execute("""
SELECT DISTINCT NB_GIRO, NB_SUBGIRO 
FROM catalogo_giros
WHERE
	NB_GIRO = 'FARMACIAS'
OR
	NB_SUBGIRO = 'DOCTORES, OTRAS ESPECIALIDADES,(MEDICOS)'
OR
	NB_SUBGIRO = 'OPTOMETRISTAS, (OFTALMOLOGOS)'
OR
	NB_SUBGIRO = 'LABORATORIOS DENTALES, (LABORATORIOS MEDICOS)'
OR
	NB_SUBGIRO = 'MEDICINAS, MEDICINAS DE PATENTE, FARMACOS DIVERSOS'
OR
	NB_SUBGIRO = 'OPTICAS, LENTES Y ANTEOJOS'
OR
	NB_SUBGIRO = 'SERVICIOS MEDICOS Y PARAMEDICOS   NO CLASIFICADOS'
ORDER BY NB_GIRO ASC;
""")

# Obtener la segunda columna del resultado de la consulta.
giros_de_interes = connector.fetchall()
giros_de_interes = [giro[1] for giro in giros_de_interes]
giros_de_interes = giros_de_interes[1:]

# Crear un dataframe con los giros de interes.
giros_de_interes = pd.DataFrame(giros_de_interes, columns=['SUBGIRO'])

# Obtener publico objetivo (personas de 65 años o más)
publico_objetivo = connector.execute("""
SELECT * FROM descripcion_cliente
WHERE EDAD >= 65;
""")

# Obtener la segunda columna del resultado de la consulta.
publico_objetivo = connector.fetchall()
publico_objetivo = [cliente[1] for cliente in publico_objetivo]

# Crear un dataframe con el publico objetivo.
publico_objetivo = pd.DataFrame(publico_objetivo, columns=['ID_CLIENTE'])

# Obtener los movimientos de los clientes de 65 años o más.
# Para los giros/subgiros de interes.

query = """
SELECT
	DISTINCT dc.NU_CTE_COD AS 'CODIGO CLIENTE',
    dc.EDAD AS 'EDAD CLIENTE',
    dc.CD_ESTADO AS 'CD_ESTADO',
    dc.CD_POSTAL AS 'CD_POSTAL',
    dc.CD_SEXO AS 'CD_SEXO',
    tc.FH_CORTE AS 'MES TRANSACCION',
    tc.FH_OPERACION AS 'DIA TRANSACCION',
    cg.NB_GIRO AS 'GIRO COMERCIAL',
    cg.NB_SUBGIRO AS 'SUBGIRO'
FROM
	descripcion_cliente AS dc
RIGHT JOIN
	transacciones_cliente AS tc
ON
	tc.NU_CTE_COD = dc.NU_CTE_COD
RIGHT JOIN
	catalogo_giros AS cg
ON
	tc.NU_AFILIACION = cg.NU_AFILIACION
WHERE
	dc.EDAD >= 65
AND
	{giro} = {data}
"""

"""""""""""""""""""""
    MOVIMIENTOS
"""""""""""""""""""""

# Implementar data
movimientos_farmacias = connector.execute(query.format(giro='cg.NB_GIRO', data="'FARMACIAS'"))
movimientos_farmacias = connector.fetchall()
movimientos_farmacias = [movimiento[0:] for movimiento in movimientos_farmacias]

# Crear un dataframe con los giros de interes.
movimientos_farmacias = pd.DataFrame(movimientos_farmacias, columns=['ID_CLIENTE', 'EDAD_CLIENTE', 'CD_ESTADO', 'CD_POSTAL', 'CD_SEXO', 'MES TRANSACCION', 'DIA TRANSACCION', 'GIRO COMERCIAL', 'SUBGIRO'])

# Implementar data
movimientos_doctores = connector.execute(query.format(giro='cg.NB_SUBGIRO', data="'DOCTORES, OTRAS ESPECIALIDADES,(MEDICOS)'"))
movimientos_doctores = connector.fetchall()
movimientos_doctores = [movimiento[0:] for movimiento in movimientos_doctores]

# Crear un dataframe con los movimientos.
movimientos_doctores = pd.DataFrame(movimientos_doctores, columns=['ID_CLIENTE', 'EDAD_CLIENTE', 'CD_ESTADO', 'CD_POSTAL', 'CD_SEXO', 'MES TRANSACCION', 'DIA TRANSACCION', 'GIRO COMERCIAL', 'SUBGIRO'])

# Implementar data
movimiento_optometristas = connector.execute(query.format(giro='cg.NB_SUBGIRO', data="'OPTOMETRISTAS, (OFTALMOLOGOS)'"))
movimiento_optometristas = connector.fetchall()
movimiento_optometristas = [movimiento[0:] for movimiento in movimiento_optometristas]

# Crear un dataframe con los movimientos.
movimiento_optometristas = pd.DataFrame(movimiento_optometristas, columns=['ID_CLIENTE', 'EDAD_CLIENTE', 'CD_ESTADO', 'CD_POSTAL', 'CD_SEXO', 'MES TRANSACCION', 'DIA TRANSACCION', 'GIRO COMERCIAL', 'SUBGIRO'])

# Implementar data
movimientos_medicinas = connector.execute(query.format(giro='cg.NB_SUBGIRO', data="'MEDICINAS, MEDICINAS DE PATENTE, FARMACOS DIVERSOS'"))
movimientos_medicinas = connector.fetchall()
movimientos_medicinas = [movimiento[0:] for movimiento in movimientos_medicinas]

# Crear un dataframe con los movimientos.
movimientos_medicinas = pd.DataFrame(movimientos_medicinas, columns=['ID_CLIENTE', 'EDAD_CLIENTE', 'CD_ESTADO', 'CD_POSTAL', 'CD_SEXO', 'MES TRANSACCION', 'DIA TRANSACCION', 'GIRO COMERCIAL', 'SUBGIRO'])

# Implementar data
movimiento_opticas = connector.execute(query.format(giro='cg.NB_SUBGIRO', data="'OPTICAS, LENTES Y ANTEOJOS'"))
movimiento_opticas = connector.fetchall()
movimiento_opticas = [movimiento[0:] for movimiento in movimiento_opticas]

# Crear un dataframe con los movimientos.
movimiento_opticas = pd.DataFrame(movimiento_opticas, columns=['ID_CLIENTE', 'EDAD_CLIENTE', 'CD_ESTADO', 'CD_POSTAL', 'CD_SEXO', 'MES TRANSACCION', 'DIA TRANSACCION', 'GIRO COMERCIAL', 'SUBGIRO'])

# Implementar data
movimientos_servicios_medicos = connector.execute(query.format(giro='cg.NB_SUBGIRO', data="'SERVICIOS MEDICOS, (CONSULTORIOS)'"))
movimientos_servicios_medicos = connector.fetchall()
movimientos_servicios_medicos = [movimiento[0:] for movimiento in movimientos_servicios_medicos]

# Crear un dataframe con los movimientos.
movimientos_servicios_medicos = pd.DataFrame(movimientos_servicios_medicos, columns=['ID_CLIENTE', 'EDAD_CLIENTE', 'CD_ESTADO', 'CD_POSTAL', 'CD_SEXO', 'MES TRANSACCION', 'DIA TRANSACCION', 'GIRO COMERCIAL', 'SUBGIRO'])


"""
ENTRENAMIENTO DEL MODELO
"""

# Crear un dataframe con los movimientos.
movimientos = pd.concat([movimientos_farmacias, movimientos_doctores, movimiento_optometristas, movimientos_medicinas, movimiento_opticas, movimientos_servicios_medicos], ignore_index=True)

# CRITERIOS DE ENTRENAMIENTO
# - Debe haber al menos 3 movimientos del mismo giro comercial o subgiro comercial en el mismo mes
# - La edad del cliente debe ser de 65 años o mas
# - A mayor cantidad de movimientos en los giros o subgiros, mayor probabilidad de que el cliente sea seleccionado como objetivo

# CLIENTE OBJETIVO
# - Cliente de 65 años o mas
# - Cliente que ha realizado al menos 3 movimientos en insumos médicos, visitas a doctores, ópticas, óptometristas, medicinas y farmacias en el mismo mes

# Creacion del modelo
modelo = LogisticRegression()



