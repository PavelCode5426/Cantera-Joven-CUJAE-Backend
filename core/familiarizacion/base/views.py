from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.models.modelosUsuario import PosibleGraduado
from custom.authentication.LDAP.ldap_manager import LDAPManager
from .serializers import ImportarPosibleGraduadoSerializer
from ...base.permissions import IsDirectorRecursosHumanos


class ImportarPosiblesGraduadosDirectorio(ListCreateAPIView):
    permission_classes = [IsDirectorRecursosHumanos]

    def list(self, request, **kwargs):
        pgraduados = LDAPManager().all_pgraduates()
        importados = PosibleGraduado.objects.filter(directorioID__in=[pgrad['areaId'] for pgrad in pgraduados])

        sin_importar = []
        for element in pgraduados:
            found = False
            it = iter(importados)
            try:
                while not found:
                    elem = next(it)
                    if elem.directorioID == element['areaId']:
                        found = True
            except StopIteration:  # SOLAMENTE SE LANZA CUANDO LLEGA AL FINAL
                sin_importar.append(element)

        return Response(sin_importar, HTTP_200_OK)

    def create(self, request, **kwargs):
        data = request.data
        serializer = ImportarPosibleGraduadoSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail': 'Posibles graduados importados correctamente'}, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
