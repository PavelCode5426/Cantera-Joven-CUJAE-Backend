#Comando para crear la imagen del backend

#Seleccionarmos la imagen base, en este caso es python
FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG FALSE
ENV LOG_FILE app.log

MAINTAINER Pavel Perez & Laura Mendez

#Creamos el directorio de trabajo
WORKDIR /code

#Copiamos los media en el directorio de trabajo
COPY . .

#Corremos el comando de instalacion de dependencias.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py" ,"runserver" ,"0.0.0.0:8000"]

