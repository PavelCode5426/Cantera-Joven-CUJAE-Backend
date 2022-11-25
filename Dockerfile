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

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8000

#Configura las variables de entorno por defecto
ENV DEBUG FALSE
ENV LOG_FILE app.log

CMD [
"python", "manage.py" ,"runserver" ,"0.0.0.0:8000",
"&",
"python" ,"manage.py","qcluster"
]

