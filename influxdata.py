'''Modulo para la obtencion de los datos almacenados en influxDB, ademas del filtrado
de etiquetas con valores de 0 constantes y sin valores.'''


#INICIALIZAR DOCKER ANTES DE CORRER ESTE SCRIPT
from influxdb import InfluxDBClient #libreria para acceder datos de la BD
import requests
import time
import pandas as pd #libreria para crear y depurar data frame
import numpy as np #libreria para optimizacion de arreglos y matrices


def generate_df(raw:str, label:str)->pd.core.frame.DataFrame:
    '''Funcion para crear un dataframe con nombre de etiqueta, fecha y valor.'''

    dic = raw['series']
    if (len(dic) > 0):
        info = dic[0]
        taken = info['values']
        df = pd.DataFrame(columns=['label','date', 'value'])
        for value in taken:
            df = df.append({'label':label, 'date':f'{value[0]}', 'value':f'{value[1]}'}, ignore_index=True)
        df['value'] = df['value'].astype(float) #convierto columna value a float
        df = df.convert_dtypes() #convierto columnas date y label a string
        return df
    else:
        df = pd.DataFrame(columns =['label', 'date', 'value'])
        return df


def get_labels(direction:str)->list:
    '''Funcion para leer y retornar una lista de etiquetas que estaban almacendas en un archivo de texto(.txt)'''
    labels = [] #arreglo de etiquetas del txt
    try: #intenta abrir la direccion del archivo
        with open (direction, "r") as file:
            for line in file:
                labels.append(line.replace("\n", "")) #quito los espacios que python lee como \n
        return labels
    except ValueError as ve: #si no puede es por que archivo existe o no se encuentra en la ruta dada
        print("Documento no encontrado")


def query(label:str)->list: #metodo para obtener informacion de etiquetas de InfluxDB
    '''Funcion para obtener los datos de influxDB de la CEIBA mediante queryes a la base de datos'''
    try: #intenta crear el cliente para recuperar los datos
        client = InfluxDBClient(host = 'localhost', port = 8086, database = 'venus') #crear el cliente para la recoleccion de los datos
        result = client.query(f'SELECT "value" FROM \"{label}\"') #recoleccion de los datos de la BD con el query
        raw = result.raw
        return raw
    except ValueError as err: #si no se puede es por que no se ha inciado docker
        print("Docker no inciado")


def get_usefull(df:pd.core.frame.DataFrame)->str: #metodo para obtener etiquetas de valores diferentes a 0
    '''Funcion para obtener etiquetas las cuales tuviesen valores distintos de 0 o vacio,
    esta funcion sirve para el filtrado de etiquetas innecesarias para enviar al servidor
    remoto'''

    try:
        if (not df.empty) and (df['value'].sum() != 0): #si el dataframe no se esta vacio y si la suma de los valores es desigual de 0
            return (df['label'][0]) #retorno la etiqueta que me es util
        else:
            return "non-valid" #retorno no valido por que es 0 o nulo
    except ValueError as ve:
        print(ve)


def write_usefull(usefull:list, direction:str): #metodo para escribir txt con etiquetas utiles
    '''Metodo para escribir en un archivo de texto las etiquetas filtradas anteriormente
    las cuales seran enviadas al servidor remoto'''

    try:
        with open (f"{direction}/usefull.txt", "w") as file:
            for label in usefull:
                file.write(f"{label}\n")
        print("file written!\n")
    except ValueError as ve:
        print(ve) 
    