'''Modulo para el envio de los datos captados por CEIBA ya sea a la 
plataforma de UniSucre o a la plataforma de UbiDots.'''


import requests
import time


def send(data:dict):
    '''Funcion para enviar los datos captados por la CEIBA a la plataforma de Unisucre
        para ser guardados y posteriormente graficados en Grafana'''

    direction = "http://181.71.69.11:4000/interfaz/httpstation" #direccion servidor Unisucre
    token= "615f007c1e563703586f2376" #token para la comunicacion
    data['token'] = token #añado la etiqueta token de conexion al diccionario entrante
    
    try:
        response = requests.post(url = direction, data = data) #hago el post de los datos a la direccion del servidor
        print(f"Respuesta del servidor: {response.text[38:]}") #respuesta del servidor
    except ValueError as ve:
        print(ve)


def sendUbiDots(data:dict):
    '''Funcion para enviar los datos captados por la CEIBA a la plataforma UbiDots'''

    device_label = "ceiba-raspberry" #nombre del espacio donde se graficaran los datos
    token = "BBFF-5JSuEt2DzidDBI3drlznGvaFhJy0u1" #token para la comunicacion
    direction = "http://industrial.api.ubidots.com" #direccion UbiDots
    direction = f"{direction}/api/v1.6/devices/{device_label}" #direccion UbiDots
    headers = {"X-Auth-Token":token, "Content-Type": "application/json"} #encabezado de la peticion a UbiDots
    try:
        request = requests.post(url = direction, headers = headers, json = data) #hago el post de los datos a la direccion de UbiDots
        status = request.status_code #status de respuesta del servidor
        time.sleep(1)
        if status >= 400: #si el status es de mas de 400 es ERORR
            print("[ERROR]")
            return False
        print("Datos enviados correctamente")
        return True
    except Exception as err:
        print(err)