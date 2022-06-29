from core.familiarizacion.base.serializers import ImportarFromDirectorioSerializer
from custom.authentication.directorio.graduado import obtenerGraduados
from core.base.models import modelosUsuario
from core.base.models import modelosSimple


class ImportarGraduadoSerializer(ImportarFromDirectorioSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if is_valid:
            try:
                self._validated_data['importar'] = set(self.initial_data['importar'])
                self._validated_data['graduados']=obtenerGraduados(self._validated_data['importar'])
            except Exception as e:
                print(e)
                is_valid = False
                self._errors.setdefault('detail','La lista contiene graduados inexistentes')
        return is_valid
    def create(self, validated_data):
        lis = list()
        for graduado_dic in validated_data['graduados']:
            area,created = modelosSimple.Area.objects.get_or_create(nombre=graduado_dic['area'])
            data = dict(
                directorioID=graduado_dic['id'],
                first_name = graduado_dic['first_name'],
                last_name = graduado_dic['last_name'],
                username = graduado_dic['username'],
                email = graduado_dic['email'],
                direccion = graduado_dic['direccion'],
                area = area,
                esExterno = graduado_dic['esExterno'],
                #lugarProcedencia = lugar, TODO Preguntar si el graduado tiene un lugar de procedencia
                esNivelSuperior = graduado_dic['esNivelSuperior']
            )
            graduado = modelosUsuario.Graduado.objects.update_or_create(directorioID=data['directorioID'],defaults=data)[0]
            lis.append(graduado)
        return lis