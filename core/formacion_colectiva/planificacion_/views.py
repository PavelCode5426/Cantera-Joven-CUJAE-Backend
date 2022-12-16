from arrow import now
from django.db.models import Max, Count
from django.http import Http404
from requests import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, get_object_or_404, CreateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.base.generics import MultiplePermissionsView
from core.base.models.modelosPlanificacion import Plan, Etapa, Comentario, Archivo
from core.base.models.modelosPlanificacionFamiliarizarcion import ActividadFamiliarizacion
from core.base.models.modelosUsuario import PosibleGraduado
from core.base.permissions import IsDirectorRecursosHumanos, IsPosibleGraduado, IsJefeArea, IsVicerrector
from core.configuracion.helpers import config
from core.formacion_colectiva.gestionar_area.serializers import PosibleGraduadoSerializer
from core.formacion_colectiva.planificacion_ import exceptions
from core.formacion_colectiva.planificacion_ import signals
from core.formacion_colectiva.planificacion_.exceptions import ResourceCantBeCommented
from core.formacion_colectiva.planificacion_.filters import ActividadColectivaFilterSet
from core.formacion_colectiva.planificacion_.helpers import can_manage_etapa, can_upload_file
from core.formacion_colectiva.planificacion_.mixin import PlanColectivoMixin, EtapaColectivaMixin, \
    ActividadColectivaMixin
from core.formacion_colectiva.planificacion_.permisions import IsSamePosibleGraduado, IsSameAreaJefeArea
from core.formacion_colectiva.planificacion_.serializers import PlanFormacionColectivaModelSerializer, \
    UpdateEstadoPlanFormacionColectivoSerializer, EtapaModelSerializer, UpdateEtapaColectivaSerializer, \
    CommentsModelSerializer, ActividadColectivaModelSerializer, CreateUpdateActividadColectivaSerializer, \
    FirmarPlanColectivoSerializer, SubirArchivoActividad, ActividadColectivaAreaModelSerializer, \
    CreateUpdateActividadAreaSerializer, ArchivoModelSerializer, ActividadAsistenciaSerilizer


class RetrieveJovenPlanColectivo(RetrieveAPIView):
    permission_classes = [IsSamePosibleGraduado | IsDirectorRecursosHumanos | IsSameAreaJefeArea | IsVicerrector]
    serializer_class = PlanFormacionColectivaModelSerializer

    def get_object(self):
        joven = self.kwargs.get('joven', get_object_or_404(PosibleGraduado, pk=self.kwargs.get('jovenID')))
        actividad = ActividadFamiliarizacion.objects.filter(asistencias=joven).first()

        if not actividad:
            plan = Plan.objects.filter(planformacion=None).order_by('-fechaCreado').first()
            if not plan: raise Http404
        else:
            plan = get_object_or_404(Plan, planformacion=None, etapas__actividades=actividad)

        return plan


class ListCreateRetrieveUpdatePlanFormacionColectivo(ModelViewSet, MultiplePermissionsView):
    serializer_class = PlanFormacionColectivaModelSerializer
    post_permission_classes = [IsDirectorRecursosHumanos]
    get_permission_classes = [IsPosibleGraduado | IsDirectorRecursosHumanos | IsJefeArea | IsVicerrector]
    put_permission_classes = [IsDirectorRecursosHumanos]
    http_method_names = ('get', 'post', 'put',)

    def get_queryset(self):
        return Plan.objects.filter(planformacion=None).order_by('-fechaCreado').all()

    def create(self, request, *args, **kwargs):
        if not config('comenzar_formacion_colectiva'):
            raise exceptions.FormacionHasNotStarted

        query = Etapa.objects.filter(etapaformacion=None).aggregate(Max('fechaFin'), Count('id', fechaFin=None))
        ultimaFechaFin = query.get('fechaFin__max')
        etapas_sinFecha = query.get('id__count')

        if ultimaFechaFin and ultimaFechaFin > now() or etapas_sinFecha:
            raise exceptions.OnlyOnePlanColectivo

        plan = Plan.objects.create()
        for i in range(1, config('etapas_plan_formacion_colectiva') + 1):
            Etapa.objects.create(plan=plan)

        serializer = self.get_serializer(instance=plan)

        signals.plan_creado.send(plan)
        return Response(serializer.data, HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateEstadoPlanFormacionColectivoSerializer(instance=instance, data=request.data)
        serializer.is_valid(True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({'detail': 'Estado del Plan actualizado correctamente'}, HTTP_200_OK)


class ListEtapasPlanFormacionColectivo(ListAPIView, PlanColectivoMixin):
    permission_classes = [IsPosibleGraduado | IsDirectorRecursosHumanos | IsJefeArea | IsVicerrector]
    serializer_class = EtapaModelSerializer

    def get_queryset(self):
        plan = self.get_plan()
        return Etapa.objects.filter(plan=plan).order_by('fechaInicio').all()


class RetrieveUpdateEtapaPlanFormacionColectivo(RetrieveModelMixin, UpdateModelMixin, GenericViewSet,
                                                MultiplePermissionsView):
    etapa_url_kwarg = 'pk'
    get_permission_classes = [IsPosibleGraduado | IsDirectorRecursosHumanos | IsJefeArea | IsVicerrector]
    put_permission_classes = [IsDirectorRecursosHumanos]
    queryset = Etapa.objects.filter(etapaformacion=None).all()
    serializer_class = EtapaModelSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        can_manage_etapa(instance)
        serializer = UpdateEtapaColectivaSerializer(instance=instance, data=request.data)
        serializer.is_valid(True)
        serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({'detail': "Etapa actualizada correctamente"})


class ListCreatePlanColectivoCommets(ListCreateAPIView, PlanColectivoMixin):
    """
    PERMITE COMENTAR Y CARGAR LOS COMENTARIOS DEL PLAN DE FORMACION FACILITANDO LA CONCILIACION PARA DESARROLLAR EL PLAN
    """
    permission_classes = (IsVicerrector | IsDirectorRecursosHumanos,)
    serializer_class = CommentsModelSerializer

    def get_queryset(self):
        plan = self.get_plan()
        return Comentario.objects.filter(plan=plan).order_by('-fecha').all()

    def create(self, request, *args, **kwargs):
        if self.plan_is_approved():
            raise ResourceCantBeCommented

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        signals.plan_comentado.send(self.get_plan())

        return Response({'detail': 'Comentario creado correctamente'}, HTTP_201_CREATED)


class ListCreateActividadColectiva(ListCreateAPIView, EtapaColectivaMixin, MultiplePermissionsView):
    get_permission_classes = [IsPosibleGraduado | IsDirectorRecursosHumanos | IsJefeArea | IsVicerrector]
    post_permission_classes = [IsDirectorRecursosHumanos]
    serializer_class = ActividadColectivaAreaModelSerializer
    filterset_class = ActividadColectivaFilterSet

    def get_queryset(self):
        etapa = self.get_etapa()
        return ActividadFamiliarizacion.objects.filter(etapa=etapa).order_by('fechaInicio').all()

    def create(self, request, *args, **kwargs):
        etapa = self.get_etapa()
        can_manage_etapa(etapa)

        serializer = CreateUpdateActividadColectivaSerializer(data=request.data)
        serializer.is_valid(True)
        serializer.save(etapa=etapa)

        return Response({'detail': 'Actividad creada correctamente'})


class RetrieveDeleteUpdateActividadColectiva(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet,
                                             MultiplePermissionsView):
    get_permission_classes = [IsPosibleGraduado | IsDirectorRecursosHumanos | IsJefeArea | IsVicerrector]
    delete_permission_classes = [IsDirectorRecursosHumanos]
    put_permission_classes = [IsDirectorRecursosHumanos]
    serializer_class = ActividadColectivaModelSerializer

    http_method_names = ('get', 'put', 'delete')

    def get_queryset(self):
        return ActividadFamiliarizacion.objects.filter(etapa__etapaformacion=None).all()

    def destroy(self, request, *args, **kwargs):
        super(RetrieveDeleteUpdateActividadColectiva, self).destroy(request, *args, **kwargs)
        return Response({'detail': "Actividad borrada correctamente"})

    def update(self, request, *args, **kwargs):
        self.serializer_class = CreateUpdateActividadColectivaSerializer
        super(RetrieveDeleteUpdateActividadColectiva, self).update(request, *args, **kwargs)
        return Response({'detail': "Actividad actualizada correctamente"})


class RetrieveDeleteUpdateActividadArea(RetrieveDeleteUpdateActividadColectiva):
    delete_permission_classes = [IsJefeArea]
    put_permission_classes = [IsJefeArea]
    serializer_class = ActividadColectivaAreaModelSerializer

    def get_queryset(self):
        area = self.request.user.area
        return ActividadFamiliarizacion.objects.filter(etapa__etapaformacion=None, area=area).all()


class FirmarPlanColectivo(CreateAPIView, PlanColectivoMixin):
    """
    """
    permission_classes = [IsVicerrector]
    serializer_class = FirmarPlanColectivoSerializer

    def create(self, request, *args, **kwargs):
        if self.plan_is_approved():
            raise exceptions.PlanAlreadyApproved

        plan = self.get_plan()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        signed = serializer.save(plan=plan, user=request.user)

        if signed:
            signals.plan_aprobado.send(plan)
            return Response({'detail': 'Plan firmado correctamente'})

        signals.plan_rechazado.send(plan)
        return Response({'detail': 'Plan rechazado correctamente'})


class ActividadColectivaUploadFile(CreateAPIView, ActividadColectivaMixin):
    """
    """
    permission_classes = [IsDirectorRecursosHumanos | IsJefeArea]
    serializer_class = SubirArchivoActividad

    def create(self, request, *args, **kwargs):
        actividad = self.get_actividad()
        can_upload_file(actividad)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        serializer.save(actividad_id=actividad.pk, plan_id=actividad.etapa.plan_id)

        return Response({'detail': 'Archivo subido correctamente'}, HTTP_201_CREATED)


class ListCreateActividadArea(ListCreateAPIView, MultiplePermissionsView, ActividadColectivaMixin):
    """
    SOLAMENTE MUESTRA LAS ACTIVIDADES DEL AREA Y CREA EN EL AREA
    """
    get_permission_classes = [IsPosibleGraduado | IsDirectorRecursosHumanos | IsVicerrector | IsJefeArea]
    post_permission_classes = [IsJefeArea]
    serializer_class = ActividadColectivaAreaModelSerializer

    def get_queryset(self):
        actividad = self.get_actividad()
        area = self.request.user.area
        return ActividadFamiliarizacion.objects.filter(actividadPadre=actividad, esGeneral=False, area=area).all()

    def create(self, request, *args, **kwargs):
        if config('planificar_formacion_colectiva'):
            raise exceptions.FormacionHasNotStarted

        actividad = self.get_actividad()
        area = request.user.area
        serializer = CreateUpdateActividadAreaSerializer(data=request.data)
        serializer.is_valid(True)
        serializer.save(etapa_id=actividad.etapa_id, actividadPadre_id=actividad.pk, area_id=area.pk)
        return Response({'detail': 'Actividad creada correctamente'})


class RetrieveDeleteArchive(RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    PERMITE GESTIONAR LOS ARCHIVOS SUBIDOS AL SISTEMA
    """
    serializer_class = ArchivoModelSerializer
    queryset = Archivo.objects.all()

    def destroy(self, request, *args, **kwargs):
        super(RetrieveDeleteArchive, self).destroy(request, *args, **kwargs)
        return Response({'detail': 'Archivo borrado correctamente'})


class ListAsistenciaActividad(ListCreateAPIView, ActividadColectivaMixin, MultiplePermissionsView):
    get_permission_classes = [IsVicerrector | IsJefeArea | IsDirectorRecursosHumanos]
    post_permission_classes = [IsJefeArea]
    serializer_class = PosibleGraduadoSerializer
    filterset_class = None  # TODO PONER UN FILTRO AQUI PARA LA ASISTENCIA

    def get_queryset(self):
        actividad = self.get_actividad()
        return actividad.asistencias.all()

    def create(self, request, *args, **kwargs):
        self.serializer_class = ActividadAsistenciaSerilizer
        serializer = self.get_serializer(instance=self.get_actividad(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Asistecia pasada correctamente'}, HTTP_201_CREATED)
