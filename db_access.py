
'''modulo para obtener los datos de las etiquetas almacenados en la base de datos influxdb'''


class Db_access:

    def __init__(self, port:int, db_name:str, host:str):
        self.__port = port
        self.__db_name = db_name
        self.__host = host


    def get_port(self) -> int:
        return self.__port


    def get_db_name(self)->str:
        return self.__db_name


    def get_host(self)->str:
        return self.__host

