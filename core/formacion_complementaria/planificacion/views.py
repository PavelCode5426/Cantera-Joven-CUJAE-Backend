from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, ListAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from core.base.generics import MultiplePermissionsView
from core.base.models.modelosPlanificacion import Comentario, Evaluacion, Archivo
from core.base.models.modelosPlanificacionFormacion import PlanFormacionComplementaria, EtapaFormacion, \
    ActividadFormacion
from core.base.models.modelosSimple import Area
from core.base.permissions import IsJefeArea, IsTutor
from core.configuracion.helpers import config
from core.formacion_complementaria.base.permissions import IsSameGraduateWhoRequestPermissions, \
    IsSameTutorWhoRequestPermissions
from core.formacion_complementaria.planificacion import signals
from core.formacion_complementaria.planificacion.exceptions import GraduateHavePlan, CantEvaluateException, \
    ResourceCantBeCommented, EvaluacionAlreadyApproved, \
    PlanAlreadyApproved
from core.formacion_complementaria.planificacion.helpers import PlainPDFExporter, PlainCalendarExporter
from core.formacion_complementaria.planificacion.mixin import PlanFormacionMixin, \
    EtapaFormacionMixinProxy, ActividadFormacionMixinProxy, PlanFormacionExportMixin
from core.formacion_complementaria.planificacion.permissions import IsGraduateTutorOrJefeAreaPermissions, \
    IsGraduateTutorPermissions, IsPlanGraduatePermissions, IsPlanTutorOrJefeAreaPermissions, IsPlanTutorPermissions, \
    IsPlanJefeArea
from core.formacion_complementaria.planificacion.serializers import PlanFormacionComplementariaModelSerializer, \
    EtapaFormacionModelSerializer, UpdateEtapaFormacionSerializer, CrearEvaluacionFormacionModelSerializer, \
    CrearEvaluacionFinalModelSerializer, CommentsModelSerializer, UpdatePlanFormacionComplementariaSerializer, \
    ArchivoModelSerializer, FirmarPlanFormacionSerializer, ActividadFormacionModelSerializer, \
    CreateUpdateActividadFormacionSerializer, CambiarEstadoActividadFormacion
from custom.authentication.models import DirectoryUser

"""
*************************
FORMACION POR PLAN
************************
"""


class ListPlanFormacionComplementariaInArea(ListAPIView):
    permission_classes = (IsJefeArea,)
    serializer_class = PlanFormacionComplementariaModelSerializer

    def get_queryset(self):
        area = get_object_or_404(Area, pk=self.kwargs['areaID'])
        return PlanFormacionComplementaria.objects.filter(graduado__area_id=area.pk).order_by('-fechaCreado').all()


class ListPlanFormacionComplementariaInTutor(ListAPIView):
    permission_classes = (IsTutor, IsSameTutorWhoRequestPermissions | IsJefeArea)
    serializer_class = PlanFormacionComplementariaModelSerializer

    def get_queryset(self):
        tutor = get_object_or_404(DirectoryUser, pk=self.kwargs['tutorID'])
        return PlanFormacionComplementaria.objects \
            .filter(graduado__tutores__tutor_id=tutor, graduado__tutores__fechaRevocado=None) \
            .order_by('-fechaCreado').all()


class CreateRetrieveGraduadoPFC(CreateAPIView, RetrieveAPIView, MultiplePermissionsView):
    """OBTENER EL PLAN DE FORMACION DADO EL GRADUADO
    - en los permisos no se verifico que sea de la misma area
    porque los tutores externos entonces no pueden revisar
    """

    post_permission_classes = (IsGraduateTutorPermissions,)
    get_permission_classes = (IsSameGraduateWhoRequestPermissions | IsGraduateTutorOrJefeAreaPermissions,)

    serializer_class = PlanFormacionComplementariaModelSerializer

    def get_object(self):
        return get_object_or_404(PlanFormacionComplementaria, graduado_id=self.kwargs['graduadoID'])

    def create(self, request, graduadoID, *args, **kwargs):
        try:
            plan = PlanFormacionComplementaria.objects.create(graduado_id=graduadoID)
            for i in range(1, config('etapas_plan_formacion_complementaria') + 1):
                EtapaFormacion(numero=i, plan=plan).save()

            serializer = self.get_serializer(plan)

            signals.plan_creado.send(plan)
            return Response(serializer.data, HTTP_201_CREATED)
        except IntegrityError as e:
            # PlanFormacionComplementaria.objects.filter(graduado_id=graduadoID).delete()
            raise GraduateHavePlan


class RetriveUpdatePlanFormacionComplementaria(RetrieveUpdateAPIView, MultiplePermissionsView, PlanFormacionMixin):
    get_permission_classes = (IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions,)
    patch_permission_classes = (IsPlanTutorPermissions,)
    serializer_class = PlanFormacionComplementariaModelSerializer
    http_method_names = ('get', 'put',)

    def get_object(self):
        return self.get_plan()

    def update(self, request, *args, **kwargs):
        self.can_manage_plan()

        plan = self.get_object()
        serializer = UpdatePlanFormacionComplementariaSerializer(instance=plan, data=request.data)
        serializer.is_valid(True)
        serializer.save()

        signals.plan_revision_solicitada.send(plan)
        return Response({'detail': 'Plan actualizado correctamente'}, HTTP_200_OK)


class ListCreatePlanFormacionCommets(ListCreateAPIView, PlanFormacionMixin):
    permission_classes = (IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions,)
    serializer_class = CommentsModelSerializer

    def get_queryset(self):
        planID = self.get_planID()
        return Comentario.objects.filter(plan_id=planID).order_by('-fecha').all()

    def create(self, request, *args, **kwargs):
        if self.plan_is_approved():
            raise ResourceCantBeCommented

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        comentario = serializer.save()

        signals.plan_comentado.send(comentario)

        return Response({'detail': 'Comentario creado correctamente'}, HTTP_201_CREATED)


class EvaluarPlanFormacion(CreateAPIView, PlanFormacionMixin):
    permission_classes = (IsPlanTutorPermissions,)
    serializer_class = CrearEvaluacionFinalModelSerializer

    def create(self, request, *args, **kwargs):
        plan = self.get_plan()
        if plan.evaluation_approved or not plan.is_approved:
            raise CantEvaluateException

        serializer = self.get_serializer(instance=plan.evaluacion_id, data=request.data)
        serializer.is_valid(raise_exception=True)
        plan.evaluacion_id = serializer.save()
        plan.save()

        signals.evaluacion_creada.send(plan)

        return Response({'detail': 'Plan evaluado correctamente'}, HTTP_200_OK)


class VersionesPlanFormacionComplementaria(ListAPIView, PlanFormacionMixin):
    permission_classes = (IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions,)
    serializer_class = ArchivoModelSerializer

    def get_queryset(self):
        planID = self.get_planID()
        return Archivo.objects.filter(plan_id=planID).order_by('-fecha').all()


class FirmarPlanFormacionComplementaria(CreateAPIView, PlanFormacionMixin):
    permission_classes = (IsPlanJefeArea,)
    serializer_class = FirmarPlanFormacionSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        if self.plan_is_approved():
            raise PlanAlreadyApproved

        plan = self.get_plan()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        signed = serializer.save(plan=plan, user=request.user)

        if signed:
            signals.plan_aprobado.send(plan)
            return Response({'detail': 'Plan firmado correctamente'})

        signals.plan_rechazado.send(plan)
        return Response({'detail': 'Plan rechazado correctamente'})


class ExportarPDFPlanFormacionComplemtaria(PlanFormacionExportMixin):
    permission_classes = [IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions]
    plain_exporter_class = PlainPDFExporter


class ExportarCalendarioPlanFormacionComplemtaria(PlanFormacionExportMixin):
    permission_classes = [IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions]
    plain_exporter_class = PlainCalendarExporter


"""
*************************
FORMACION POR ETAPAS
************************
"""


class ListEtapasPlanFormacionComplementaria(ListAPIView, PlanFormacionMixin):
    permission_classes = [IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions]
    serializer_class = EtapaFormacionModelSerializer

    def get_queryset(self):
        planID = self.get_planID()
        return EtapaFormacion.objects.filter(plan_id=planID).order_by('numero').all()


class RetrieveUpdateEtapaFormacion(RetrieveUpdateAPIView, EtapaFormacionMixinProxy, MultiplePermissionsView):
    put_permission_classes = [IsPlanTutorPermissions]
    get_permission_classes = [IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions]
    serializer_class = EtapaFormacionModelSerializer

    http_method_names = ('get', 'put')

    def get_object(self):
        return self.get_etapa()

    def update(self, request, *args, **kwargs):
        self.can_manage_etapa()

        instance = self.get_object()
        serializer = UpdateEtapaFormacionSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, HTTP_200_OK)


class EvaluarEtapaFormacion(CreateAPIView, EtapaFormacionMixinProxy):
    # TODO LISTAR PLANES PENDIENTES POR EVALUAR Y APROBAR LA EVALUACION POR EL PLAN
    permission_classes = (IsPlanTutorPermissions,)
    serializer_class = CrearEvaluacionFormacionModelSerializer

    def get_object(self):
        return self.get_etapa()

    def create(self, request, *args, **kwargs):
        etapa = self.get_object()
        plan = self.get_plan()
        etapas_sin_evaluar = plan.etapas.filter(etapaformacion__numero__lt=etapa.numero,
                                                etapaformacion__evaluacion=None).count()
        if etapa.evaluation_approved or not plan.is_approved and etapas_sin_evaluar:
            raise CantEvaluateException

        serializer = self.get_serializer(instance=etapa.evaluacion, data=request.data)
        serializer.is_valid(raise_exception=True)
        evaluacion = serializer.save()
        if not etapa.evaluacion:
            etapa.evaluacion_id = evaluacion.pk
            etapa.save()
            signals.evaluacion_creada.send(etapa)
        else:
            signals.evaluacion_actualizada.send(etapa)

        return Response({'detail': 'Etapa evaluada correctamente'}, HTTP_200_OK)


"""
****************
EVALUACIONES
****************
"""


# TODO MOSTRAR LAS EVALUACIONES PENDIENTES

class AprobarEvaluacion(CreateAPIView):
    permission_classes = (IsPlanJefeArea,)

    def create(self, request, evaluacionID, *args, **kwargs):
        evaluacion = get_object_or_404(Evaluacion, pk=evaluacionID)

        if evaluacion.aprobadoPor_id is not None:
            raise EvaluacionAlreadyApproved

        evaluacion.aprobadoPor = request.user
        signals.evaluacion_aprobada.send(evaluacion)
        return Response({'detail', 'Evaluacion aprobada correctamente'}, HTTP_200_OK)


"""
****************
TAREA DE FORMACION
****************
"""


class ListCreateActividadFormacion(ListCreateAPIView, MultiplePermissionsView, ActividadFormacionMixinProxy):
    """
    PARA CREAR ADICIONAR TAREAS A LAS ETAPAS EL PLAN NO DEBE ESTAR APROBADO NI LA ETAPA DEBE ESTAR EVALUADA
    """
    get_permission_classes = [IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions]
    post_permission_classes = [IsPlanTutorPermissions]
    serializer_class = ActividadFormacionModelSerializer

    def get_queryset(self):
        etapaID = self.get_etapaID()
        return ActividadFormacion.objects.filter(etapa_id=etapaID, actividadPadre=None).all()

    def create(self, request, *args, **kwargs):
        self.can_manage_etapa()

        etapa = self.get_etapa()
        serializer = CreateUpdateActividadFormacionSerializer(data=request.data)
        serializer.is_valid(True)
        serializer.save(etapa=etapa)
        return Response({'detail': 'Actividad creada correctamente'})


class RetrieveUpdateDeleteActividadFormacion(RetrieveUpdateDestroyAPIView, MultiplePermissionsView,
                                             ActividadFormacionMixinProxy):
    get_permission_classes = [IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions]
    delete_permission_classes = [IsPlanTutorPermissions]
    put_permission_classes = [IsPlanTutorPermissions]
    patch_permission_classes = [IsPlanTutorPermissions]

    serializer_class = ActividadFormacionModelSerializer

    def get_object(self):
        return self.get_actividad()

    def update(self, request, *args, **kwargs):
        self.can_manage_actividad()
        actividad = self.get_object()
        serializer = CreateUpdateActividadFormacionSerializer(instance=actividad, data=request.data)
        serializer.is_valid(True)
        serializer.save()

        if getattr(actividad, '_prefetched_objects_cache', None):
            actividad._prefetched_objects_cache = {}

        return Response({'detail': 'Actividad actualizada correctamente'})

    def partial_update(self, request, plan, *args, **kwargs):
        self.can_change_actividad_status()
        actividad = self.get_object()
        serializer = CambiarEstadoActividadFormacion(instance=actividad, data=request.data)
        serializer.is_valid(True)
        serializer.save()

        if getattr(actividad, '_prefetched_objects_cache', None):
            actividad._prefetched_objects_cache = {}

        signals.actividad_revisada.send(actividad)
        return Response({'detail': 'Actividad actualizada correctamente'})

    def destroy(self, request, *args, **kwargs):
        self.can_manage_actividad()
        super(RetrieveUpdateDeleteActividadFormacion, self).destroy(request, *args, **kwargs)
        return Response({'detail': 'Actividad borrada correctamente'})


class ListCreateActividadFormacionCommets(ListCreateAPIView):
    """
    LOS COMENTARIOS A LAS ACTIVIDADES SE HACE UNA VEZ APROBADO EL PLAN
    """
    permission_classes = (IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions,)
    serializer_class = CommentsModelSerializer

    def get_queryset(self):
        actividadID = self.kwargs['actividadID']
        return Comentario.objects.filter(actividad_id=actividadID).order_by('-fecha').all()

    def create(self, request, plan, actividadID, *args, **kwargs):
        etapa = get_object_or_404(EtapaFormacion, actividades=actividadID)
        if not plan.is_approved or etapa.evaluacion_id is not None:
            raise ResourceCantBeCommented

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        comentario = serializer.save()

        signals.actividad_comentada.send(comentario)

        return Response({'detail': 'Comentario creado correctamente'}, HTTP_201_CREATED)


# TODO CREAR LAS SUBTAREAS DEL PLAN
class ListCreateSubActividadFormacion(ListCreateAPIView):
    pass
