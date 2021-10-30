import influxdata as idata
import senddata as send
import mongodata as mongo
import mqtt 
import threading
import time


def getData(raw:list)->tuple:
    '''Funcion para obtener y retornar el ultimo dato con la fecha y hora respectivas 
    almacenado en influxDB de todas las etiquetas'''

    dic = raw['series'] 
    if (len(dic)>0):
        info = dic[0]
        taken = info['values']
        date_hour_value = taken[-1] #Obtengo lista con par fecha-hora y valor 
        date = date_hour_value[0][:10] #substring de 0 a 10 para obtener la fecha
        hour = date_hour_value[0][14:19] #substring para obtener la hora
        value = date_hour_value[1] #valor en la posicion 1 de la lista
        return date, hour, value #retorno tupla con fecha, hora y valor del ultimo dato de InfluxDB


def ceiba(): 
    '''Esta funcion se encraga de hacer todo lo de la ceiba. 
    Funcion para obtener los datos de influxDB, esta funcion recorre una lista
    de etiquetas recuperando los datos de cada una de estas etiquetas, luego guarda
    estos datos en un BD local para despues enviarlos a un servidor remoto.'''
        
    labels = { #diccionario que cambia el nombre convencional de la etiqueta por el nombre que admite el servidor remoto
       "battery/Dc/0/Current" : "corriente_bat", 
       "battery/Dc/0/Voltage" : "voltaje_bat", 
       "system/Dc/Battery/Power":"potencia_bat",
       "solarcharger/Dc/0/Current":"corriente_Mppt",
       "solarcharger/Dc/0/Voltage":"voltaje_Mppt",
       "solarcharger/Pv/V":"voltajepanel_Mppt",
       "solarcharger/Pv/I":"corrientepanel_Mppt",
       "solarcharger/State":"est_estacion_Mppt",
       "solarcharger/Yield/Power":"yielpower_Mppt",
       "vebus/Ac/Out/P":"ac_output_inversor",
    }

    data = { #diccionario de etiquetas y valores a guardar y enviar
        'corriente_bat':None,
        'voltaje_bat':None,
        'potencia_bat': None,
        'corriente_Mppt':None,
        'voltaje_Mppt':None,
        'voltajepanel_Mppt':None,
        'corrientepanel_Mppt':None,
        'est_estacion_Mppt':None,
        'yielpower_Mppt':None,
        'ac_output_inversor':None
    }

    for label in labels.keys(): #recorro la lista de etiquetas
        raw = idata.query(label) #hago query para obtener datos de influxDB
        label_ts = labels[label] #cambio el nombre de la etiqueta
        date_hour_value = getData(raw) #obtengo el ultimo dato almacenado con la fecha y hora respectivas de influxDB
        data[label_ts] = date_hour_value[2] #escribo en el diccionario el valor de la etiqueta
    send.send(data) #envio los datos a UniSucre
    mongo.writeMongo(data, date_hour_value,collection="victron") #escribo los datos de la CEIBA en la BD


def ceiba_run(): 
    '''Funcion para ejecutar todos los procesos
    involucrado en la toma de datos de la ceiba en un
    loop infinito cada x tiempo'''
    while(True):
        ceiba()
        time.sleep(60) #cada 60 segundos ejecutar


if __name__ == '__main__':
    #uso multithreading para, en un hilo correr el bucle infinito de ceiba
    #y en otro hilo correr bucle infinito de sensores
    t1 = threading.Thread(target=ceiba_run) #hilo1 con ceiba
    t2 = threading.Thread(target=mqtt.mqtt_run) #hilo2 con sensores
    t2.start() #ejecuto hilo2 primero para que haya data de sensores en mongo
    t1.start() #ejecuto hilo1 segundo para poder recolectar y enviar la data de sensores