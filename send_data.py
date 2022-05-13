'''Modulo para el envio de los datos captados por la CEIBA ya sea a la 
plataforma de UniSucre o a UbiDots.'''


__author__ = "Juan Pablo Giraldo Perez, Santiago Puerta Florez"


import requests
import time


def send_uni_sucre(to_be_send:dict) -> None:
    """Envia los datos captados por la CEIBA a la plataforma de Unisucre
  
    Args:
        to_be_send (dict):[Diccionario de datos a enviar a la plataforma
        de UniSucre]
    """

    http_direction = "http://181.57.149.36:4000/interfaz/httpstation" #direccion servidor Unisucre
    token = "621cdb72928dd822d476f8f2" #token para la comunicacion
    to_be_send['token'] = token #añado la etiqueta token de conexion al diccionario entrante
    
    try:
        response_from_server = requests.post(url = http_direction, data = to_be_send) #hago el post de los datos a la direccion del servidor
        print(f"Respuesta del servidor UniSucre: {response_from_server.text[38:]}") #respuesta del servidor
    except ValueError as error:
        print(error)


def send_ubi_dots(to_be_send:dict) -> boolean:
    """Envia los datos captados por la CEIBA a la plataforma UbiDotsç
    
    Args:
        to_be_send (dict): [Diccionario de datos a enviar a UbiDots]
        
    Returns:
        boolean
    """
    
    graphs_space_name = "ceiba-raspberry" #nombre del espacio donde se graficaran los datos
    token = "BBFF-5JSuEt2DzidDBI3drlznGvaFhJy0u1" #token para la comunicacion
    http_direction = "http://industrial.api.ubidots.com" #direccion UbiDots
    http_direction = f"{http_direction}/api/v1.6/devices/{graphs_space_name}" #direccion UbiDots
    request_headers = {"X-Auth-Token":token, "Content-Type": "application/json"} #encabezado de la peticion a UbiDots
    try:
        request = requests.post(url = http_direction, headers = request_headers, json = to_be_send) #hago el post de los datos a la direccion de UbiDots
        request_status = request.status_code #status de respuesta del servidor
        time.sleep(1)
        if request_status >= 400: #si el status es de mas de 400 es ERORR
            print("[ERROR]")
            return False
        print(f"Respuesta del servidor UbiDots: {request.text[38:41]}")
        return True
    except Exception as err:
        print(err)


def send_to_available(to_be_send:dict)-> boolean:
    """Intenta enviar los datos a la plataforma de UniSucre si no lo logra
       trata de enviar los datos a UbiDots
    Args:
        to_be_send (dict): [Diccionario de datos a enviar a la plataforma
        de UniSucre o, en caso de fallo, a UbiDots]
    
    Returns:
        boolean
    """"
    try:
        send_uni_sucre(to_be_send=to_be_send)
    except ValueError as error:
        #si no puede mandar a uniSucre lo mas probable es que el servidor no se encuentre disponible
        send_ubi_dots(to_be_send=to_be_send)
