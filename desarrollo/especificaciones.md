# Energética 2030
En este repositorio se encuentran los módulos con el código desarrollado e implementado para el correcto funcionamiento del Living Lab.

## A tener en cuenta para el correcto funcionamiento del código
### Los siguientes son requisitos a tener en cuenta para el correcto funcionamiento del código contenido en este repositorio.
! *Tener presente que el código aquí expuesto esta pensado para **ser utilizado en una RaspBerryPi**, para que así, esta se puede conectar con el Color Control del Living Lab.*
* Se recomienda en primera instancia, el instalar python y con este, el usar un entorno virtual para descargar las librerías usadas en el desarrollo, que serán mencionadas a continuación.
	
	| Nombre de la librería | Modulo donde se usa | Preinstalada en el sistema |Mayor información|
	|-----------------------| --------------------|----------------------------|-----------------|
	| influxdb              | influx_database     |<center>[]</center>         |https://pypi.org/project/influxdb/
	| paho-mqtt             | mqtt                |<center>[]</center>         | https://pypi.org/project/paho-mqtt/
	| pymongo		| mongodb	      |<center>[]</center>         | https://pypi.org/project/pymongo/
	| requests		| send_data	      |<center>[]</center>         | https://pypi.org/project/requests/
	| time 			| send_data           |<center>[x]</center>        | https://pypi.org/project/python-time/
	| threading	        | run		      |<center>[x]</center>        | https://pypi.org/project/threaded/
	| datetime		| mqtt		      |<center>[x]</center>        | https://pypi.org/project/DateTime/
	| sys			| mqtt	              |<center>[x]</center>        | https://docs.python.org/3/library/sys.html
	| ssl 		        | mqtt 	  	      |<center>[x]</center>        | https://pypi.org/project/ssl/

* En segunda medida es necesaria **la instalación de Docker** en la RaspBerry véase [este enlace](https://blog.desdelinux.net/como-instalar-docker-en-raspberry-pi-con-raspbian/) para mayor referencia. Luego de instalado Docker, es necesario el **incorporar los contenedores de Victron Energy** *para la comunicación con el Color Control*, visite [este enlace](https://github.com/victronenergy/venus-docker-grafana) para la instalación. 
* Finalmente es necesario el **instalar MongoDb** en la RaspBerry, *crear la base de datos y crear las respectivas colecciones*; en nuestro caso lo haremos haciendo uso de un contenedor de Docker. Para la instalación de MongoDb siga los pasos listados a continuación. 
		<pre><code>pi@raspberry:~ $ sudo docker images
		REPOSITORY 			 TAG	     IMAGE ID	     CREATED	     SIZE
		casualsimulation/rpi-mongodb3    latest      bce4db2845c7    2 years ago     366MB
		pi@raspberry:~ $ sudo docker run -d -p 27017:27017 --name mongoDB casualsimulation/rpi-mongodb3 
		pi@raspberry:~ $ sudo docker start mongoDB
		pi@raspberry:~ $ sudo docker exec -it mongoDB bash
		root@47aaee89ccc0:/data# mongo</code></pre>
		! Al completar estos pasos ya **tendrás un contenedor Docker con MongoDb corriendo.** Ahora crearemos la base de datos y las colecciones donde se almacenaran los datos.
		<pre><code>\> use livingLab 
		switch to db livingLab
		\> db.createCollection("victron")
		{ "ok" : 1 }
		\> db.createCollection("sensors")
		{ "ok" : 1 }</code></pre>
		! Finalmente tienes la base de datos con sus colecciones creadas.
		
## Ejecución del código
### Prerrequisitos:
Antes de proceder con la ejecución del código, revisa que cuentas con los siguientes requisitos:

1. Poseer una instalación de Python en el dispositivo. 
2. Poseer una instalación de Docker en el dispositivo.
3. Poseer los contenedores de Victron Energy operativos en el dispositivo.
4. Poseer un contenedor con MongoDb operativo en el sistema.

Una vez que se cuenta con lo anterior podemos proceder a la ejecución del código. Para la correcta ejecución del código sigue los siguientes pasos:

1. Iniciar los contenedores de Victron Energy, así como el contendor con MongoDb.
	<pre><code> pi@raspberry:~ $ cd Desktop
	pi@raspberry:~/Desktop $ sudo docker-compose up --detach
	pi@raspberry:~/Desktop $ sudo docker start mongoDB</code></pre>
2. Conectar mediante red el Color Control y el dispositivo de ejecución del código, en preferencia una RaspBerryPi.
3. Si se ha hecho uso de un entorno virtual, inicializarlo.
	<pre><code> pi@raspberry:~/Desktop $ cd ceiba
	pi@raspberry:~/Desktop/ceiba $ source venv/bin/activate
	(venv) pi@raspberry:~/Desktop/ceiba $</code></pre>
4. Ejecutar el código.
	<pre><code>(venv) pi@raspberry:~/Desktop/ceiba $ python3 run.py</code></pre>
