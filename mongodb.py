
'''Modulo para escribir datos en una coleccion mongodb
   nombre de la base de datos: livingLab
   nombre de las colecciones: victron, sensors 
   -> victron, es la coleccion que almacena los datos de la CEIBA
   -> sensors, es la coleccion que almacena los datos de los sensores de temperatura y humedad.'''


__author__ = "Juan Pablo Giraldo Perez, Santiago Puerta Florez"


import db_access as db
import pymongo


class Mongodb(db.Db_access):
    """Hereda de un DAO: Data Access Object; Representa un objeto para 
       escribir datos en una coleccion MongoDB
       
       Attributes:
        port (int): [Puerto de la base de datos para lectura/escritura]
        db_name (str): [Nombre de la base de datos]
        host (str): [Host de la base de datos]
        collection_name (str): [Nombre de la coleccion MongoDB de la cual se van a leer datos]
       """
    
    

    def __init__(self, port: int, db_name: str, host: str, collection_name: str) -> None:
        """Inicializa el objeto de tipo Mongodb
        
        Args:
           port (int): [Puerto de la base de datos para lectura/escritura]
            db_name (str): [Nombre de la base de datos]
            host (str): [Host de la base de datos]
            collection_name (str): [Nombre de la coleccion MongoDB de la cual se van a leer datos] 
        """
        super().__init__(port = port, db_name = db_name, host=host)
        self.__collection_name = collection_name


    def get_collection_name(self) -> str:
        """"Retorna el nombre de la coleccion del objeto tipo Mongodb
        
        Args:
            self(Mongodb)
            
        Returns:
            str
        """
        return self.__collection_name


    def connect_to_mongo(self)->pymongo.collection.Collection:
        '''Establece una conexion con la base de datos
        
        Args:
            self(Mongodb)
        
        Returns:
            mongo_collection(pymongo.collection.Collection): [Cliente para poder hacer
            CRUD en una coleccion de la base de datos]
        '''
        try:
            mongo_client = pymongo.MongoClient(self.get_host(),self.get_port()) #cliente de la base de datos
            mongo_collection = mongo_client[self.get_db_name()][self.get_collection_name()] #coleccion en la que escribir los datos
            return mongo_collection
        except Exception as error:
            print(error)


    def write_to_mongo(self, db_entry:dict, date_hour_value:tuple) -> None:
        '''Escribir datos a una coleccion MongoDB
        
        Args:
            self(Mongodb)
            db_entry(dict): [Diccionario con datos a montar en la coleccion MongoDB]
            date_hour_value(tuple): [Tupla con fecha, hora, valor]
       '''

        db_entry['fecha'] = date_hour_value[0]
        db_entry['hora'] = date_hour_value[1]
        print(db_entry)

        try:
            mongo_collection = self.connect_to_mongo() #direccion en la que escribir los datos
            mongo_collection.insert_one(db_entry) #escribir en la base de datos el diccionario
            print ("coleccion guardada!")
        except Exception as err:
            print ("error guardando en la coleccion!")
