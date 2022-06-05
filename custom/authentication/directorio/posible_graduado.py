from rest_framework.generics import ListCreateAPIView

from custom.authentication.models import DirectoryUser
from core.base.models.modelosUsuario import PosibleGraduado


posible_graduado = [
    {'id': 1, 'email': 'perezpavel5426@gmail.com', 'username': 'pperez', 'password': '1234', 'first_name': 'Pavel',
     'last_name': 'Perez Gonzalez', 'lugarProcedencia': 'CUJAE'},
    {'id': 2, 'email': 'lauramendezdelpino@gmail.com', 'username': 'laura', 'password': '1234', 'first_name': 'Laura',
     'last_name': 'Mendez del Pino', 'lugarProcedencia': 'UCI'},
    {'id': 3, 'email': 'usuarurio10@gmail.com', 'username': 'lmendez', 'password': '3333', 'first_name': 'Beyli',
     'last_name': 'Mendez', 'lugarProcedencia': 'Universidad de la Haban'},
    {'id': 4, 'email': 'pepef@gmail.com', 'username': 'pepef', 'password': '3434', 'first_name': 'Pepe',
     'last_name': 'Ferro Leo', 'lugarProcedencia': 'Tecnológico'}
]

class ListarPosiblesGraduados(ListCreateAPIView):
    def posible_graduado_list(self, request, *args, **kwargs):
        pg = PosibleGraduado.objects.all()
        if request.method == 'GET':
            results = [
                {
                    posible_graduado['id']: pg.directorioID,
                    posible_graduado['firt_name']: pg.first_name,
                    posible_graduado['last_name']: pg.last_name,
                    posible_graduado['email']: pg.email,
                    posible_graduado['username']: pg.username,
                    posible_graduado['password']: pg.password,
                    posible_graduado['anno_academico']: pg.lugarProcedencia,
                } for pg in posible_graduado]

        return {"count": len(results), "pg": results}



