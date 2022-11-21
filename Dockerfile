#Comando para crear la imagen del backend

#Seleccionarmos la imagen base, en este caso es python
FROM python:3.7-alpine

MAINTAINER Pavel Perez & Laura Mendez

#Creamos el directorio de trabajo
WORKDIR /code

#Copiamos los archivos en el directorio de trabajo
COPY . .

#Corremos el comando de instalacion de dependencias.
RUN pip install -r requirements.txt
