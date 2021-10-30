'''Modulo para la escritura y lectura de los datos alamacenados en la base de datos
no relacional MongoDB que esta en la RaspBerryPi.
Nombre de la base de datos: livingLab
Nombre de las colecciones: 
-> victron, coleccion que almacena todos los datos de la CEIBA
-> sensors, coleccion que almacena todos los datos de los sensores de temperatura y humedad.'''


import pymongo


def connectDB(port: int, db_name:str, collection: str)->pymongo.collection.Collection:
    '''Funcion que sirve para establecer una conexion a la coleccion de la base de datos deseada
    y retorna el cliente para poder leer o escribir datos en la base de datos'''
    try:
        client = pymongo.MongoClient('localHost',port) #cliente que escribira en la BD
        collect = client[db_name][collection] #coleccion en la que escribir los datos
        return collect
    except Exception as err:
        print(err)


def writeMongo(db_entry:dict, date_hour_value:tuple, collection:str, db_name:str="livingLab", port:int = 27017):
    '''Funcion para escribir datos tanto de CEIBA como de sensores; recibe como parametros
    la fecha, hora, etiqueta, valor, nombre de la base de datos y nombre de la coleccion
    en donde se guardaran los datos.'''

    db_entry['fecha'] = date_hour_value[0]
    db_entry['hora'] = date_hour_value[1]
    print(db_entry)

    try:
        collect = connectDB(port, db_name, collection) #direccion en la que escribir los datos
        collect.insert_one(db_entry) #escribir en la base de datos el diccionario
        print ("Coleccion guardada")
    except Exception as err:
        print ("Error guardando en la coleccion")


def readMongo(collection:str, db_name:str = "livingLab", port:int = 27017)->list:
    '''Funcion para leer datos de sensores; recibe como parametros
    el nombre de la base de datos, puerto y nombre de la coleccion en donde se
    guardaran los datos.'''

    documents = [] #lista para almacenar todas las colecciones de datos de la BD
    try:
        collect = connectDB(port, db_name, collection) #conexion con la BD
        collections = collect.find({}) #tomo todas la colecciones
        for collection in collections: #recorro coleccion por coleccion
            documents.append(collection) #añado coleccion por coleccion a la lista
        print (documents) #retorno lista de colecciones
    except Exception as err:
        print(err)