'''modulo principal del programa y entry point del sistema, este modulo se encarga de orquestar y manejar los demas modulos del sistema
para el correcto funcionamiento ejecuta todo lo de la CEIBA y a su vez todo lo de los sensores MQTT.'''


import influx_database as influx
import send_data
import mongodb as mongo
#import mqtt 
import threading
import time


def read_influx_sensors_and_send(influxdb_object:influx.Influxdb, mongodb_object:mongo.Mongodb): 
    '''Este metodo se encarga de hacer todo lo de la ceiba. 
        Obtener los datos de influxDB, esta funcion recorre una lista
        de etiquetas recuperando los datos de cada una de estas etiquetas, luego envia estos datos a un servidor remoto y
        posteriormente de enviados los almacena en una base de datos.'''
        
    change_label_to_remote_accepted = { #diccionario que cambia el nombre convencional de la etiqueta por el nombre que admite el servidor remoto
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

    label_values_to_be_send_and_saved = { #diccionario de etiquetas y valores a guardar y enviar
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

    for label in change_label_to_remote_accepted.keys(): #recorro la lista de etiquetas
        name_of_label_to_send = change_label_to_remote_accepted[label] #cambio el nombre de la etiqueta
        date_hour_value = influxdb_object.get_last_label_data(label) #obtengo el ultimo dato almacenado con la fecha y hora respectivas de influxDB
        label_values_to_be_send_and_saved[name_of_label_to_send] = date_hour_value[2] #escribo en el diccionario el valor de la etiqueta
    send_data.send_to_available(label_values_to_be_send_and_saved) #envio los datos a la platofarma que este disponible 
    mongodb_object.write_to_mongo(label_values_to_be_send_and_saved, date_hour_value) #escribo los datos de la CEIBA en la BD


def ceiba_main(): 
    '''metodo para ejecutar todos los procesos
    involucrado en la toma de datos de la ceiba en un
    loop infinito cada x tiempo'''
    influxdb_object = influx.Influxdb(port = 8086, db_name = "venus", host = "localhost")
    mongodb_object = mongo.Mongodb(port = 27017, db_name = "livingLab", host = "localhost", collection_name="victron")
    while(True):
        read_influx_sensors_and_send(influxdb_object,mongodb_object)
        time.sleep(60) #cada 60 segundos ejecutar


if __name__ == '__main__':
    '''uso multithreading para, en un hilo correr el bucle infinito de ceiba
    y en otro hilo correr bucle infinito de sensores'''
    t1 = threading.Thread(target=ceiba_main) #hilo1 con ceiba
    #t2 = threading.Thread(target=mqtt.mqtt_run) #hilo2 con sensores
    #t2.start() #ejecuto hilo2 primero para que haya data de sensores en mongo
    t1.start() #ejecuto hilo1 segundo para poder recolectar y enviar la data de sensores