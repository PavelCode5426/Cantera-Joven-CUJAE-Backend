from annoying.functions import get_object_or_None
from django.contrib.auth.models import Group
from django.db import transaction

from core.base.models.modelosUsuario import PosibleGraduado
from core.base.serializers import ImportarFromDirectorioSerializer
from custom.authentication.LDAP.ldap_facade import LDAPFacade
from custom.authentication.models import DirectoryUser


class ImportarPosibleGraduadoSerializer(ImportarFromDirectorioSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if is_valid:
            try:
                pgraduados_carnet = set(self.initial_data['importar'])
                pgraduados = LDAPFacade().all_pgraduates()
                pgraduados = list(filter(lambda x: x['identification'] in pgraduados_carnet, pgraduados))

                if len(pgraduados) != len(pgraduados_carnet):
                    raise Exception  # EXCEPCION CUANDO FALTE ESTUDIANTES POR ENCONTRAR

                self._validated_data['importar'] = pgraduados_carnet
                self._validated_data['pgraduados'] = pgraduados
            except Exception:
                self._errors.setdefault('detail', 'La lista contiene posibles graduados inexistentes')

        return not bool(self._errors)

    def create(self, validated_data):
        lis = list()
        role = Group.objects.get(name='POSIBLE GRADUADO')
        with transaction.atomic():
            for pgraduado_dic in validated_data['pgraduados']:
                data = dict(
                    directorioID=pgraduado_dic['areaId'],
                    first_name=pgraduado_dic['name'],
                    last_name=f"{pgraduado_dic['surname']} {pgraduado_dic['lastname']}",
                    username=pgraduado_dic['user'],
                    carnet=pgraduado_dic['identification'],
                    email=pgraduado_dic.get('email', None),
                    direccion=pgraduado_dic.get('address', None),
                    cargo=pgraduado_dic.get('teachingCategory', None),
                    telefono=pgraduado_dic.get('phone', None),
                    area=None,
                )

                usuario = get_object_or_None(DirectoryUser, carnet=data['carnet'])
                pgraduado = PosibleGraduado.objects.update_or_create(directoryuser_ptr=usuario, defaults=data)[0]
                pgraduado.groups.add(role)
                lis.append(pgraduado)
        transaction.commit()
        return lis
