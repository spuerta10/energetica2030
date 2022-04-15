
'''modulo para obtener los datos de las etiquetas almacenados en la base de datos influxdb'''


import db_access as db
from influxdb import InfluxDBClient  #libreria para acceso a los datos de influxdb


class Influxdb(db.Db_access):
    '''Hereda de un DAO: Data Access Object; Representa un objeto para lectura
    de la base de datos InfluxDBç
    
    Args:
        instance (Influxdb): [Si hay un objeto Influxdb ya creado; si no 
        hay ningun objeto Influxdb creado es None]
        port (int): [Puerto de la base de datos para lectura/escritura]
        db_name (str): [Nombre de la base de datos]
        host (str): [Host de la base de datos]
        '''
    
    __instance = None #si no hay objetos creados = None
                      #si hay objetos creados = objeto Influxdb creado
                      #patron de diseño Singleton
    def __new__(cls, port:int, db_name:str, host:str) -> None:
        """Crea el objeto de tipo Influxdb
        
        Args:
            instance (Influxdb): [Si hay un objeto Influxdb ya creado; si no 
            hay ningun objeto Influxdb creado es None]
            port (int): [Puerto de la base de datos para lectura/escritura]
            db_name (str): [Nombre de la base de datos]
            host (str): [Host de la base de datos] 
        """
        if Influxdb.__instance is None: #si no hay ninguna instacia creada;
                                        #patron de diseño Singleton
            Influxdb.__instance = object.__new__(cls)
        Influxdb.__instance.port = port
        Influxdb.__instance.db_name = db_name
        Influxdb.__instance.host = host
        return Influxdb.__instance #retorna siempre la misma instancia
    
    
    def read_influxdb_data(self, label_to_search:str)->list:
        '''Obtiene todos los datos de una etiqueta almacenada en la base de datos 
           Influxdb
        
        Args:
            self (Influxdb)
            label_to_search (str): [Etiqueta a ser buscada en la base de datos]
        
        Returns:
            all_label_data (list): [Lista con todos los datos hallados de
            label_to_search]
        '''

        try: #intenta obtener los datos de la base de datos
            influxdb_client = InfluxDBClient(host = self.get_host(), port = self.get_port(), database = self.get_db_name()) #crear el cliente para la recoleccion de los datos
            query_result = influxdb_client.query(f'SELECT "value" FROM \"{label_to_search}\"') #recoleccion de los datos de la BD con el query
            all_label_data = query_result.raw
            return all_label_data
        except ValueError as error: #si no se puede es altamente probable que sea por que no se ha inciado docker
            print(f"docker no iniciado! {error}")


    def get_last_label_data(self, label_to_search:str)->tuple:
        """Obtiene y retorna el ultimo dato escrito en la base de datos  
           de una etiqueta dada
         
         Args:
            label_to_search (str): [Etiqueta a ser buscada en la base de datos]
         
         Returns:
            date_hour_value (tuple): [Tupla que contiene la fecha, hora y valor del
            ultimo dato registrado en la base de datos de la label_to_search]
         """

        all_label_data = self.read_influxdb_data(label_to_search)
        all_label_data_list = all_label_data['series'] 
        if (len(all_label_data_list)>0):
            label_values_dict = all_label_data_list[0]
            all_label_date_hour_value = label_values_dict['values']
            label_last_date_hour_value = all_label_date_hour_value[-1] #Obtengo lista con par fecha-hora y valor 
            date = label_last_date_hour_value[0][:10] #substring de 0 a 10 para obtener la fecha
            hour = label_last_date_hour_value[0][14:19] #substring para obtener la hora
            value = label_last_date_hour_value[1] #valor en la posicion 1 de la lista
            return date, hour, value #retorno tupla con fecha, hora y valor del ultimo dato de InfluxDB
