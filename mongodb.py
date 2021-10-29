
'''modulo para escribir datos en una coleccion de mongodb
nombre de la base de datos: livingLab
nombre de las colecciones: victron, sensors 
    -> victron, es la coleccion que almacena los datos de la CEIBA
    -> sensors, es la coleccion que almacena los datos de los sensores de temperatura y humedad.'''


import db_access as db
import pymongo


class Mongodb(db.Db_access):

    def __init__(self, port, db_name, host, collection_name):
        super().__init__(port = port, db_name = db_name, host=host)
        self.__collection_name = collection_name


    def get_collection_name(self):
        return self.__collection_name


    def connect_to_mongo(self)->pymongo.collection.Collection:
        '''metodo para establecer una conexion a la base de datos, 
            retorna el cliente para poder hacer CRUD en una coleccion de la base de datos'''
        try:
            mongo_client = pymongo.MongoClient(self.get_host(),self.get_port()) #cliente de la base de datos
            mongo_collection = mongo_client[self.get_db_name()][self.get_collection_name()] #coleccion en la que escribir los datos
            return mongo_collection
        except Exception as error:
            print(error)


    def write_to_mongo(self, db_entry:dict, date_hour_value:tuple):
        '''Funcion para escribir datos tanto de CEIBA como de sensores; recibe como parametros
        la fecha, hora, etiqueta, valor, nombre de la base de datos y nombre de la coleccion
        en donde se guardaran los datos.'''

        db_entry['fecha'] = date_hour_value[0]
        db_entry['hora'] = date_hour_value[1]
        print(db_entry)

        try:
            mongo_collection = self.connect_to_mongo() #direccion en la que escribir los datos
            mongo_collection.insert_one(db_entry) #escribir en la base de datos el diccionario
            print ("coleccion guardada!")
        except Exception as err:
            print ("error guardando en la coleccion!")