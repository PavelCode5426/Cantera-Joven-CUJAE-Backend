from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from rest_framework import serializers
from core.base.models.modelosTutoria import GraduadoTutor,SolicitudTutorExterno
from core.base.models.modelosUsuario import Graduado
from core.base.models.modelosSimple import Area
from core.formacion_complementaria.gestionar_solicitar_tutor.helpers import get_tutor
from custom.authentication.serializer import DirectoryUserSerializer
from custom.authentication.models import DirectoryUser


class GraduadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduado
        fields = ('id','username','first_name','last_name','email','direccion','esExterno','esNivelSuperior','aval')

class TutoresDelGraduadoSerializer(serializers.ModelSerializer):
    tutor = DirectoryUserSerializer()
    class Meta:
        model = GraduadoTutor
        exclude = ['graduado']
        deph = 1

class GraduadosDelTutorSerializer(serializers.ModelSerializer):
    graduado = GraduadoSerializer()
    class Meta:
        model = GraduadoTutor
        exclude = ['tutor']
        deph = 1

class AsignarSolicitarTutorSerializer(serializers.Serializer):
    tutores = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    areas_solicitadas = serializers.PrimaryKeyRelatedField(many=True,read_only=True)

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        has_aval = False
        try:
            has_aval = self.initial_data['graduado'].aval
        except ObjectDoesNotExist:
            self._errors.setdefault('graduado', 'Es requerido tener aval para otorgar tutores')

        if is_valid \
                and (not ('areas_solicitadas' in self.initial_data or 'tutores' in self.initial_data) \
                or not (len(self.initial_data['areas_solicitadas']) or len(self.initial_data['tutores']))):
            self._errors.setdefault('detail','Necesita declara al menos un atributo')
        elif is_valid:
            area = self.initial_data['graduado'].area
            self._validated_data['graduado']=self.initial_data['graduado']
            if 'tutores' in self.initial_data:
                ids = set(self.initial_data['tutores'])
                tutores = DirectoryUser.objects.filter(pk__in=ids,area=area,graduado=None,posiblegraduado=None,estudiante=None).all()
                if len(tutores) is not len(ids) or not len(ids):
                    self._errors.setdefault('tutores', 'Se han seleccionado tutores incorrectamente')
                else:self._validated_data['tutores'] = tutores

            if 'areas_solicitadas' in self.initial_data:
                ids = set(self.initial_data['areas_solicitadas'])
                areas = Area.objects.filter(pk__in=ids).exclude(pk=area.pk).all()
                if len(areas) is not len(ids):
                    self._errors.setdefault('areas_solicitadas', 'Se han seleccionado areas incorrectamente')
                else: self._validated_data['areas_solicitadas']=areas

        return not bool(self._errors)

    def create(self, validated_data):
        result = {}
        graduado = validated_data['graduado']

        if 'tutores' in validated_data:
            tutores = validated_data['tutores']
            graduado.tutores.exclude(tutor__in=tutores).update(fechaRevocado=now())
            tutoresList = list()
            for tutor in tutores:
                tutoresList.append(graduado.tutores.get_or_create(tutor=tutor,graduado=graduado,fechaRevocado=None))
            result['tutores'] = tutoresList

        if 'areas_solicitadas' in validated_data:
            areas = validated_data['areas_solicitadas']
            graduado.solicitudes.filter(area__in=areas,fechaRespuesta=None).update(fechaCreado=now())
            solicitudesList = list()
            for area in areas:
                solicitudesList.append(graduado.solicitudes.get_or_create(area=area,graduado=graduado))
            result['areas_solicitadas'] = solicitudesList

        return result

class SolicitudTutorExternoSerializer(serializers.ModelSerializer):
    area = serializers.SerializerMethodField()
    graduado = GraduadoSerializer()

    def get_area(self,instance):
        return instance.area.nombre

    class Meta:
        model = SolicitudTutorExterno
        fields = '__all__'
        depth = 1

class ResponderSolicitudSerializer(serializers.Serializer):
    asignar = serializers.PrimaryKeyRelatedField(read_only=True,default=None,allow_null=True)

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid()

        if is_valid and self.initial_data['asignar']:
            tutor = get_tutor(self.initial_data['asignar'],area=self.initial_data['area'])
            if not tutor:
                self._errors['asignar']='Tutor no encontrado'
            else:
                self._validated_data['asignar']=tutor

        return not bool(self._errors)
    def create(self, validated_data):
        solicitud = validated_data['solicitud']
        solicitud.respuesta = 'asignar'in validated_data and validated_data['asignar'] is not None
        solicitud.fechaRespuesta = now()

        if solicitud.respuesta:
            tutor = validated_data['asignar']
            solicitud.graduado.tutores.create(tutor=tutor,graduado=solicitud.graduado,fechaRevocado=None)

        solicitud.save()
        return solicitud






