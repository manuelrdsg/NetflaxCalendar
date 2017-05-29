# Netflax Calendar

## Descripción

Si siempre te pierdes tus series favoritas en Netflix, utilizando *Netflax Calendar* se actualizará tu calendario de Google cada vez que la cuenta ***@gallonetflix*** tuitee la fecha de salida de una nueva serie en dicha plataforma.

## Participantes

- Manuel Rodríguez-Sanchez Guerra
- Luis Gonzaga Rozo Bueno

## Metodo de uso

Pare ejecutar la aplicación es necesario tener instalados las siguientes librerías Python: *Celery, Dropbox, Tweepy, Google Calendar*, además de rabbitmq u otro broker. El programa corre sobre **Python3**.

1. Ejecutar rabbitmq, para esto lazaremos el siguiente comando
	```
	sudo rabbitmq-server
    ```
    
2. Lanzar el worker de celery, para esto, estando situados en la carpeta raiz del proyecto ejecutaremos el siguiente comando
	```
	celery -A server woker --loglevel=info
    ```

3. Lanzar el steaming de twitter, para esto ejecutaremos el fichero python *twitter.py*
	```
	python3 twitter.py
    ```
    
4. Ejecutar el programa que nos actualize el calendario una vez que se hayan publicado tweets nuevos
	```
	python3 calen.py
    ```