'''modulo para el envio de los datos captados por la CEIBA ya sea a la 
plataforma de UniSucre o a la plataforma de UbiDots.'''


import requests
import time


def send_uni_sucre(to_be_send:dict):
    '''metodo para enviar los datos captados por la CEIBA a la plataforma de Unisucre
        para ser guardados y posteriormente graficados en Grafana'''

    http_direction = "http://181.71.69.11:4000/interfaz/httpstation" #direccion servidor Unisucre
    token = "615f007c1e563703586f2376" #token para la comunicacion
    to_be_send['token'] = token #añado la etiqueta token de conexion al diccionario entrante
    
    try:
        response_from_server = requests.post(url = http_direction, data = to_be_send) #hago el post de los datos a la direccion del servidor
        print(f"Respuesta del servidor UniSucre: {response_from_server.text[38:]}") #respuesta del servidor
    except ValueError as error:
        print(error)


def send_ubi_dots(to_be_send:dict):
    '''metodo para enviar los datos captados por la CEIBA a la plataforma
        de UbiDots'''
    
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


def send_to_available(to_be_send:dict):
    try:
        send_uni_sucre(to_be_send=to_be_send)
    except ValueError as error:
        #si no puede mandar a uniSucre lo mas probable es que el servidor no se encuentre disponible
        send_ubi_dots(to_be_send=to_be_send)
