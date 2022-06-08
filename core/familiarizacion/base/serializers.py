from rest_framework import serializers
from custom.authentication.directorio.estudiante import obtenerEstudiantes
from custom.authentication.directorio.posibleGraduado import obtenerPosibleGraduados
from core.base.models import modelosUsuario
from core.base.models import modelosSimple


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
            data = dict(
                directorioID=estudiante_dic['id'],
                first_name = estudiante_dic['first_name'],
                last_name = estudiante_dic['last_name'],
                username = estudiante_dic['username'],
                email = estudiante_dic['email'],
                direccion = estudiante_dic['direccion'],
                anno_academico = estudiante_dic['anno']
            )
            estudiante = modelosUsuario.Estudiante.objects.update_or_create(directorioID=data['directorioID'],defaults=data)[0]
            lis.append(estudiante)
        return lis

class ImportarPosibleGraduadoSerializer(ImportarFromDirectorioSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if is_valid:
            try:
                self._validated_data['importar'] = set(self.initial_data['importar'])
                self._validated_data['posibleGraduado'] = obtenerPosibleGraduados(self._validated_data['importar'])
            except Exception as e:
                print(e)
                is_valid = False
                self._errors.setdefault('detail', 'La lista contiene posibles graduados inexistentes')
        return is_valid
    def create(self, validated_data):
        lis = list()
        for posibleGraduado_dic in validated_data['posibleGraduado']:
            lugarProcedencia = modelosSimple.LugarProcedencia.objects.get_or_create(nombre=posibleGraduado_dic['lugarProcedencia'])[0]
            data = dict(
                directorioID=posibleGraduado_dic['id'],
                first_name=posibleGraduado_dic['first_name'],
                last_name=posibleGraduado_dic['last_name'],
                username=posibleGraduado_dic['username'],
                email=posibleGraduado_dic['email'],
                direccion=posibleGraduado_dic['direccion'],
                lugarProcedencia = lugarProcedencia
            )
            posibleGraduado = modelosUsuario.PosibleGraduado.objects.update_or_create(directorioID=data['directorioID'],defaults=data)[0]
            lis.append(posibleGraduado)
        return lis