from rest_framework import serializers
from custom.authentication.directorio.estudiante import obtenerEstudiantes
from core.base.models import modelosUsuario, modelosSimple


class ImportarFromDirectorioSerializer(serializers.Serializer):
    importar = serializers.ListField(required=True)

class ImportarEstudianteSerializer(ImportarFromDirectorioSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if is_valid:
            try:
                self._validated_data['importar'] = set(self.initial_data['importar'])
                self._validated_data['estudiantes']=obtenerEstudiantes(self._validated_data['importar'])
            except Exception as e:
                print(e)
                is_valid = False
                self._errors.setdefault('detail','La lista contiene estudiantes inexistentes')
        return is_valid
    def create(self, validated_data):
        lis = list()
        for estudiante_dic in validated_data['estudiantes']:
            area, created = modelosSimple.Area.objects.get_or_create(nombre=estudiante_dic['area'])
            data = dict(
                directorioID=estudiante_dic['id'],
                first_name = estudiante_dic['first_name'],
                last_name = estudiante_dic['last_name'],
                username = estudiante_dic['username'],
                email = estudiante_dic['email'],
                direccion = estudiante_dic['direccion'],
                anno_academico = estudiante_dic['anno'],
                area = area,
            )
            estudiante = modelosUsuario.Estudiante.objects.update_or_create(directorioID=data['directorioID'],defaults=data)[0]
            lis.append(estudiante)
        return lis

