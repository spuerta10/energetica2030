import ssl
import sys
import paho.mqtt.client
import mongodata as mongo
from datetime import datetime
import threading


def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='#', qos=2)


def on_message(client, userdata, message):
	count = 0
	data = {}
	print('------------------------------')
	print('topic: %s' % message.topic)
	print('payload: %s' % message.payload)
	data['topic'] = message.topic
	data['payload'] = str(message.payload)[2:-1]
	today = str(datetime.today())
	date_hour = (today[:10], today[11:19], 0) #value no importa
	mongo.writeMongo(data, date_hour, "sensors") #escribo el valor del topic en mongo


def mqtt_run():
	client = paho.mqtt.client.Client(client_id='puerta-pc', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='192.168.0.159', port=1883) #direccion IP de la raspberry y puerto de escucha de mosquitto
	client.loop_forever()


if __name__ == "__main__":
	mqtt_run()
