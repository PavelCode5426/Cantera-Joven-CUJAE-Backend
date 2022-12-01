from django.contrib.auth.models import Group
from django.db import transaction

from core.base.models.modelosUsuario import Estudiante
from core.base.serializers import ImportarFromDirectorioSerializer
from custom.authentication.LDAP.ldap_manager import LDAPManager


class ImportarEstudianteSerializer(ImportarFromDirectorioSerializer):

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if is_valid:
            try:
                estudiantes_carnet = set(self.initial_data['importar'])
                area = self.initial_data['area']
                estudiantes = LDAPManager().all_students_from_area(area)
                estudiantes = list(filter(lambda x: x['identification'] in estudiantes_carnet, estudiantes))

                if len(estudiantes) != len(estudiantes_carnet):
                    raise Exception  # EXCEPCION CUANDO FALTE ESTUDIANTES POR ENCONTRAR

                self._validated_data['importar'] = estudiantes_carnet
                self._validated_data['estudiantes'] = estudiantes
                self._validated_data['area'] = area
            except Exception:
                self._errors.setdefault('detail', 'La lista contiene estudiantes inexistentes')

        return not bool(self._errors)

    def create(self, validated_data):
        lis = list()
        area = validated_data['area']
        role = Group.objects.get(name='ESTUDIANTE')
        with transaction.atomic():
            for estudiante_dic in validated_data['estudiantes']:
                data = dict(
                    directorioID=estudiante_dic['areaId'],
                    first_name=estudiante_dic['name'],
                    last_name=f"{estudiante_dic['surname']} {estudiante_dic['lastname']}",
                    username=estudiante_dic['user'],
                    carnet=estudiante_dic['identification'],
                    email=estudiante_dic['email'],
                    direccion=estudiante_dic['address'],
                    anno_academico=estudiante_dic.get('studentYear', None),
                    cargo=estudiante_dic.get('teachingCategory', None),
                    telefono=estudiante_dic.get('phone', None),
                    area=area,
                )
                estudiante = Estudiante.objects.update_or_create(directorioID=data['directorioID'], defaults=data)[0]
                estudiante.groups.add(role)
                lis.append(estudiante)
        transaction.commit()
        return lis
