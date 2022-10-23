import pandas as pd
import mysql.connector

class BaseDatos:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            port="3307",
            user="root",
            passwd="adminroot",
            database="hackathon_bbva"
        )
        self.connector = self.mydb.cursor()

    def obtener_giros_de_interes(self):
        """
        CON BASE EN EL ANÁLSIS REALIZADO DE LOS ARCHIVOS CSV SE CONCLUYÓ QUE
        LOS GIROS Y SUB GIROS DE INTERÉS SON:

            - GIRO: FARMACIAS

            - SUBGIRO: 'DOCTORES, OTRAS ESPECIALIDADES,(MEDICOS)'
            - SUBGIRO: 'OPTOMETRISTAS, (OFTALMOLOGOS)'
            - SUBGIRO: 'LABORATORIOS DENTALES, (LABORATORIOS MEDICOS)'
            - SUBGIRO: 'MEDICINAS, MEDICINAS DE PATENTE, FARMACOS DIVERSOS'
            - SUBGIRO: 'OPTICAS, LENTES Y ANTEOJOS'
            - SUBGIRO: 'SERVICIOS MEDICOS Y PARAMEDICOS (NO CLASIFICADOS)'

            :return: lista de giros y subgiros de interés
        """

        query = """
            SELECT 
                DISTINCT NB_GIRO, NB_SUBGIRO 
            FROM
                catalogo_giros
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
        """

        response = self.connector.execute(query)

        giros_de_interes = self.connector.fetchall()
        giros_de_interes = [giro[1] for giro in giros_de_interes]

        return giros_de_interes

    def obtener_publico_objetivo(self):
        """
        EL PÚBLICO OBJETIVO ES EL DE PERSONAS DE 65 AÑOS O MÁS

            :return: lista de 
        """
        query = """
            SELECT
                *
            FROM
                descripcion_cliente
            WHERE
                EDAD >= 65
        """

        response = self.connector.execute(query)

        publico_objetivo = self.connector.fetchall()
        publico_objetivo = [cliente[0:] for cliente in publico_objetivo]

        return publico_objetivo

    def obtener_clientes(self):
        """
        OBTENEMOS TODOS LOS CLIENTES DE LA BASE DE DATOS

            :return: lista de clientes
        """
        query = """
            SELECT
                *
            FROM
                descripcion_cliente
        """

        response = self.connector.execute(query)

        clientes = self.connector.fetchall()
        clientes = [cliente[0:] for cliente in clientes]

        return clientes

    def movimientos_objetivo(self):
        """
        SE OBTENDRÁN LOS MOVIMIENTOS BANCARIOS QUE SERVIRÁN
        COMO FLAGS PARA ALERTAR SOBRE UN POSIBLE NUEVO
        CLIENTE OBJETIVO
        """

        query = """
            SELECT
                dc.NU_CTE_COD AS 'CODIGO CLIENTE',
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
                cg.NB_SUBGIRO = '{data}'
        """

        giros_de_interes = self.obtener_giros_de_interes()

        objetivos = []
        
        for giro in giros_de_interes:
            self.connector.execute(query.format(data=giro))
            objetivo = self.connector.fetchall()

            objetivo = [cliente[0:] for cliente in objetivo]
            objetivos.append(objetivo)

        return objetivos

    def obtener_movimientos(self):
        """
        OBTENEMOS TODOS LOS MOVIMIENTOS DE LAS PERSONAS
        DE 65 AÑOS O MÁS
        """

        query = """
            SELECT
                dc.NU_CTE_COD AS 'CODIGO CLIENTE',
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
            -- IGNORE NULL VALUES
            WHERE
                dc.NU_CTE_COD IS NOT NULL
            LIMIT 50;
        """

        self.connector.execute(query)

        movimientos = self.connector.fetchall()
        movimientos = [movimiento[0:] for movimiento in movimientos]

        return movimientos


# TEST
if __name__ == '__main__':
    bd = BaseDatos()
    test_movimientos_objetivo = bd.movimientos_objetivo()
    print(test_movimientos_objetivo)