
"""Modulo para recibir datos de los sensores de temperatura y humedad mediante el protocolo de comunicacion
	mqtt y guardar estos datos en una coleccion MongoDB"""

import ssl
import sys
import paho.mqtt.client
import mongodb
from datetime import datetime


def receive_mqtt_messages(client, userdata, flags, rc) -> None:
	'''Recibe los mensajes de un determinado topic mediante mqtt
	
	Args:
		client: [Instancia del cliente que hace el llamado]
		userdata: [Datos de cualquier tipo definidos por el usuario]
		flags: [Banderas de respuesta enviadas por el broker]
		rc: [El resultado de la conexion]
	'''
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='#', qos=2)


def write_mongo_message_data(client, userdata, message) -> None:
	'''Escribe los mensajes recibidos en la coleccion MongoDB
	
	Args:
		client: [Instancia del cliente que hace el llamado]
		userdata: [Datos de cualquier tipo definidos por el usuario]
		message: [Instancia de mensaje MQTT que contiene: topic, payload
		qos, retain]
	
	'''
	to_be_written_mongo = {} #datos a ser escritos en mongo
	print('------------------------------')
	print('topic: %s' % message.topic)
	print('payload: %s' % message.payload)
	to_be_written_mongo['topic'] = message.topic
	to_be_written_mongo['payload'] = str(message.payload)[2:-1]
	date_hour_seconds = str(datetime.today())
	date_hour_value = (date_hour_seconds[:10], date_hour_seconds[11:19], 0) #value no importa
	mongodb_object = mongodb.Mongodb(port = 27017, db_name = "livingLab", host = "localhost", collection_name="sensors")
	mongodb_object.write_to_mongo(to_be_written_mongo, date_hour_value) #escribo el valor del topic en mongo


def start_mqtt_communication():
	'''Inicia la comunicacion y recepcion de mensajes'''
	mqtt_client = paho.mqtt.client.Client(client_id='puerta-pc', clean_session=False)
	mqtt_client.on_connect = receive_mqtt_messages
	mqtt_client.on_message = write_mongo_message_data
	mqtt_client.connect(host='192.168.0.159', port=1883) #direccion IP de la raspberry y puerto de escucha de mosquitto
	mqtt_client.loop_forever()


if __name__ == "__main__":
	start_mqtt_communication()
