import requests
from rest_framework.generics import ListCreateAPIView
from custom.authentication.models import DirectoryUser
from core.base.models.modelosUsuario import Estudiante


estudiantes = [
    {'id': 1, 'email': 'perezpavel5426@gmail.com', 'username': 'pperez', 'password': '1234', 'first_name': 'Pavel',
     'last_name': 'Perez Gonzalez', 'anno_academico': '3'},
    {'id': 2, 'email': 'lauramendezdelpino@gmail.com', 'username': 'laura', 'password': '1234', 'first_name': 'Laura',
     'last_name': 'Mendez del Pino', 'anno_academico': '2'},
    {'id': 3, 'email': 'usuarurio10@gmail.com', 'username': 'lmendez', 'password': '3333', 'first_name': 'Beyli',
     'last_name': 'Mendez', 'anno_academico': '3'},
    {'id': 4, 'email': 'pepef@gmail.com', 'username': 'pepef', 'password': '3434', 'first_name': 'Pepe',
     'last_name': 'Ferro Leo', 'anno_academico': '4'}
]

class ListarEstudiantes(ListCreateAPIView):
    def estudiantes_list(self, request, *args, **kwargs):
        est = Estudiante.objects.all()
        if request.method == 'GET':
         results = [
            {
                estudiantes['id']: est.directorioID,
                estudiantes['firt_name']: est.first_name,
                estudiantes['last_name']: est.last_name,
                estudiantes['email']: est.email,
                estudiantes['username']: est.username,
                estudiantes['password']: est.password,
                estudiantes['anno_academico']: est.anno_academico,
            } for est in estudiantes]
         return {"count": len(results), "est": results}

