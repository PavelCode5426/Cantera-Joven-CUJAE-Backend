# Guia de despliegue

Para desplegar el backend siga atentamente los siguientes pasos en dependencia de donde desea desplegar la aplicacion.

### Despliegue en local

Para desplegar de forma local necesita cumplir con los siguientes requisitos.

#### Requisitos de depliegue:

* Python 3.9
* Postgresql 14

#### Guia de despliegue:

1. Crear entorno vitural.

```shell
py -m venv venv
```

2. Activar entorno virtual.

```shell
cd venv/Scripts

activate
```

3. Moverse hacia el directorio de la aplicacion mediante la terminal.

```shell
cd ../..
```

4. Instalar dependencias.

```shell
pip install requirements.txt
```

5. Crear archivo **.env** para configurar las variables de entorno.

6. Abrir archivo con un editor de texto, copiar y configurar las siguientes variables de entorno

```text
#FRAMEWORK CONFIGURATION
DEBUG= ?
SECRET_KEY= ?

#EMAIL CONFIGURATION
DEFAULT_FROM_EMAIL= ?
EMAIL_HOST= ?
EMAIL_PORT= ?
EMAIL_HOST_USER= ?
EMAIL_HOST_PASSWORD= ?

#LOGS AND ERROR TELEGRAM CHANNEL
TELEGRAM_CHANNEL= ?
TELEGRAM_TOKEN= ?

```

7. Correr migraciones y migrar

```shell
py manage.py makemigrations
py manage.py migrate
```

8. Levantar servidor local

```shell
py manage.py runserver
```

9. Levantar proceso de tareas asincronas

```shell
py manage.py qcluster
```

### Despliegue con Docker