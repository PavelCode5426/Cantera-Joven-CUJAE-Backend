from annoying.functions import get_object_or_None
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import serializers

from core.base.models.modelosSimple import Area
from core.base.models.modelosUsuario import Graduado
from core.familiarizacion.base.serializers import ImportarFromDirectorioSerializer
from custom.authentication.LDAP.ldap_facade import LDAPFacade, is_supergraduate
from custom.authentication.models import DirectoryUser


class ImportarGraduadoSerializer(ImportarFromDirectorioSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if is_valid:
            try:
                graduados_carnet = set(self.initial_data['importar'])
                graduados = LDAPFacade().all_graduates()
                graduados = list(filter(lambda x: x['identification'] in graduados_carnet, graduados))

                if len(graduados) != len(graduados_carnet):
                    raise Exception  # EXCEPCION CUANDO FALTE ESTUDIANTES POR ENCONTRAR

                self._validated_data['importar'] = graduados_carnet
                self._validated_data['graduados'] = graduados
            except Exception:
                self._errors.setdefault('detail', 'La lista contiene graduados inexistentes')

        return not bool(self._errors)

    def create(self, validated_data):
        lis = list()
        areas = dict()

        for area in Area.objects.all():
            areas[area.distinguishedName] = area

        role = Group.objects.get(name='GRADUADO')
        with transaction.atomic():
            for graduado_dic in validated_data['graduados']:
                data = dict(
                    directorioID=graduado_dic['areaId'],
                    first_name=graduado_dic['name'],
                    last_name=f"{graduado_dic['surname']} {graduado_dic['lastname']}",
                    username=graduado_dic['user'],
                    carnet=graduado_dic['identification'],
                    email=graduado_dic['email'],
                    direccion=graduado_dic['address'],
                    cargo=graduado_dic.get('teachingCategory', None),
                    telefono=graduado_dic.get('phone', None),
                    area=areas[graduado_dic['area']],
                    esNivelSuperior=is_supergraduate(graduado_dic),
                    esExterno=bool(graduado_dic['personExternal'])
                )

                usuario = get_object_or_None(DirectoryUser, carnet=data['carnet'])
                graduado = Graduado.objects.update_or_create(directoryuser_ptr=usuario, defaults=data)[0]
                graduado.groups.add(role)
                lis.append(graduado)
        transaction.commit()
        return lis


class ImportarTutorSerializer(ImportarFromDirectorioSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if is_valid:
            try:
                tutores_carnet = set(self.initial_data['importar'])
                area = self.initial_data['area']
                tutores = LDAPFacade().all_tutors_from_area(area)
                tutores = list(filter(lambda x: x['identification'] in tutores_carnet, tutores))

                if len(tutores) != len(tutores_carnet):
                    raise Exception  # EXCEPCION CUANDO FALTE TUTORES POR ENCONTRAR

                self._validated_data['importar'] = tutores_carnet
                self._validated_data['tutores'] = tutores
                self._validated_data['area'] = area
            except Exception:
                self._errors.setdefault('detail', 'La lista contiene tutores inexistentes')

        return not bool(self._errors)

    def create(self, validated_data):
        lis = list()
        area = validated_data['area']
        role = Group.objects.get(name='TUTOR')
        with transaction.atomic():
            for tutor_dic in validated_data['tutores']:
                data = dict(
                    directorioID=tutor_dic['areaId'],
                    first_name=tutor_dic['name'],
                    last_name=f"{tutor_dic['surname']} {tutor_dic['lastname']}",
                    username=tutor_dic['user'],
                    carnet=tutor_dic['identification'],
                    email=tutor_dic['email'],
                    direccion=tutor_dic['address'],
                    cargo=tutor_dic.get('teachingCategory', None),
                    telefono=tutor_dic.get('phone', None),
                    area=area,
                )

                tutor = DirectoryUser.objects.update_or_create(carnet=tutor_dic['identification'], defaults=data)[0]
                tutor.groups.add(role)
                lis.append(tutor)
        transaction.commit()
        return lis


class GraduadoSerializer(serializers.ModelSerializer):
    aval = serializers.SerializerMethodField()
    plan = serializers.SerializerMethodField()

    def get_aval(self, object):
        return hasattr(object, 'aval')

    def get_plan(self, object):
        return hasattr(object, 'planformacioncomplementaria')

    class Meta:
        model = Graduado
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'direccion', 'cargo', 'telefono', 'carnet',
            'directorioID', 'area', 'esExterno', 'esNivelSuperior', 'aval',
            'plan')
