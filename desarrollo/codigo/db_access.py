
"""Módulo para crear un DAO: Data Access Object"""


__author__ = "Juan Pablo Giraldo Perez, Santiago Puerta Florez"


class Db_access:
    """Representa un DAO: Data Access Object;
       objeto para el acceso a una base de datos.
    
    Attributes:
        port (int): [Puerto de la base de datos para lectura/escritura]
        db_name(str): [Nombre de la base de datos]
        host: [Host de la base de datos]
    """
    

    def __init__(self, port:int, db_name:str, host:str) -> None:
        """Inicializa el objeto de tipo Db_access
        
        Args: 
            port (int): [Puerto de la base de datos para lectura/escritura]
            db_name (str): [Nombre de la base de datos]
            host (str): [Host de la base de datos]
        """
        self.__port = port
        self.__db_name = db_name
        self.__host = host


    def get_port(self) -> int:
        """Retorna el puerto del objeto tipo Db_access
        
        Args:
            self (Db_access)
        
        Rerturns:
            int
        """
        return self.__port


    def get_db_name(self)->str:
        """Retorna el nombre de la base de datos del objeto tipo Db_access
        
        Args:
            self (Db_access)
        
        Returns:
            str
        """
        return self.__db_name


    def get_host(self)->str:
        """Retorna el host del objeto tipo Db_access
        
        Args:
            self (Db_access)
        
        Returns:
            str
        """
        return self.__host

