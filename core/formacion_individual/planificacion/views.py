from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, ListAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet

from core.base.generics import MultiplePermissionsView
from core.base.models.modelosPlanificacion import Comentario, Evaluacion, Archivo
from core.base.models.modelosPlanificacionFormacion import EtapaFormacion, \
    ActividadFormacion, PlanFormacion
from core.base.models.modelosSimple import Area, PropuestaMovimiento
from core.base.permissions import IsJefeArea, IsTutor
from core.configuracion.helpers import config
from core.formacion_individual.base.helpers import user_is_student
from core.formacion_individual.base.permissions import IsSameJovenWhoRequestPermissions, \
    IsSameTutorWhoRequestPermissions
from core.formacion_individual.planificacion import signals
from core.formacion_individual.planificacion.exceptions import JovenHavePlan, CantEvaluateException, \
    ResourceCantBeCommented, PlanAlreadyApproved, EvaluacionAlreadyApproved, FormacionHasNotStarted
from core.formacion_individual.planificacion.helpers import PlainPDFExporter, PlainCalendarExporter
from core.formacion_individual.planificacion.mixin import PlanFormacionMixin, PlanFormacionExportMixin, \
    ActividadFormacionMixin, EtapaFormacionMixin
from core.formacion_individual.planificacion.permissions import IsJovenTutorOrJefeAreaPermissions, \
    IsJovenTutorPermissions, IsPlanJovenPermissions, IsPlanTutorOrJefeAreaPermissions, IsPlanTutorPermissions, \
    IsPlanJefeArea
from core.formacion_individual.planificacion.serializers import PlanFormacionModelSerializer, \
    EtapaFormacionModelSerializer, UpdateEtapaFormacionSerializer, CrearEvaluacionFormacionModelSerializer, \
    CrearEvaluacionFinalModelSerializer, CommentsModelSerializer, UpdatePlanFormacionSerializer, \
    ArchivoModelSerializer, FirmarPlanFormacionSerializer, ActividadFormacionModelSerializer, \
    CreateUpdateActividadFormacionSerializer, CambiarEstadoActividadFormacion, SubirArchivoActividad, \
    EvaluacionModelSerializer, PropuestaMovimientoModelSerializer
from core.formacion_individual.planificacion.signals import actividad_revision_solicitada
from custom.authentication.models import DirectoryUser

"""
*************************
FORMACION POR PLAN
************************
"""


class ListPlanFormacionInArea(ListAPIView):
    permission_classes = (IsJefeArea,)
    serializer_class = PlanFormacionModelSerializer

    def get_queryset(self):
        area = get_object_or_404(Area, pk=self.kwargs['areaID'])
        return PlanFormacion.objects.filter(joven__area_id=area.pk).order_by('-fechaCreado').all()


class ListPlanFormacionInTutor(ListAPIView):
    permission_classes = (IsTutor, IsSameTutorWhoRequestPermissions | IsJefeArea)
    serializer_class = PlanFormacionModelSerializer

    def get_queryset(self):
        tutor = get_object_or_404(DirectoryUser, pk=self.kwargs['tutorID'])
        return PlanFormacion.objects \
            .filter(joven__tutores__tutor_id=tutor, joven__tutores__fechaRevocado=None) \
            .order_by('-fechaCreado').all()


class CreateRetrieveJovenPlanFormacion(CreateAPIView, RetrieveAPIView, MultiplePermissionsView):
    """
    PERMITE OBTENER Y CREAR EL PLAN DE FORMACION DADO UN JOVEN

    OBTENER EL PLAN DE FORMACION DADO EL GRADUADO
    - en los permisos no se verifico que sea de la misma area
    porque los tutores externos entonces no pueden revisar
    """

    post_permission_classes = (IsJovenTutorPermissions,)
    get_permission_classes = (IsSameJovenWhoRequestPermissions | IsJovenTutorOrJefeAreaPermissions,)

    serializer_class = PlanFormacionModelSerializer

    def get_object(self):
        return get_object_or_404(PlanFormacion, joven_id=self.kwargs['jovenID'], evaluacion=None)

    def create(self, request, *args, **kwargs):
        joven = kwargs.get('joven')

        if not config('comenzar_formacion_complementaria'):
            raise FormacionHasNotStarted

        if PlanFormacion.objects.filter(joven=joven, evaluacion=None).exists():
            raise JovenHavePlan

        plan = PlanFormacion.objects.create(joven=joven)
        if user_is_student(joven):
            config_key = 'etapas_plan_formacion_individual_estudiante'
        else:
            config_key = 'etapas_plan_formacion_individual_graduado'

        for i in range(1, config(config_key) + 1):
            EtapaFormacion(numero=i, plan=plan).save()

        serializer = self.get_serializer(plan)

        signals.plan_creado.send(plan)
        return Response(serializer.data, HTTP_201_CREATED)


class RetriveUpdatePlanFormacion(RetrieveUpdateAPIView, MultiplePermissionsView, PlanFormacionMixin):
    """
    PERMITE OBTENER EL PLAN DE FORMACION INDIVIDUAL Y PERMITE CAMBIAR EL ESTADO DEL MISMO
    """
    get_permission_classes = (IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions,)
    patch_permission_classes = (IsPlanTutorPermissions,)
    serializer_class = PlanFormacionModelSerializer
    http_method_names = ('get', 'put',)

    def get_object(self):
        return self.get_plan()

    def update(self, request, *args, **kwargs):
        self.can_manage_plan()

        plan = self.get_object()
        serializer = UpdatePlanFormacionSerializer(instance=plan, data=request.data)
        serializer.is_valid(True)
        serializer.save()

        signals.plan_revision_solicitada.send(plan)
        return Response({'detail': 'Plan actualizado correctamente'}, HTTP_200_OK)


class ListCreatePlanFormacionCommets(ListCreateAPIView, PlanFormacionMixin):
    """
    PERMITE COMENTAR Y CARGAR LOS COMENTARIOS DEL PLAN DE FORMACION FACILITANDO LA CONCILIACION PARA DESARROLLAR EL PLAN
    """
    permission_classes = (IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions,)
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

        signals.plan_comentado.send(self.get_plan())

        return Response({'detail': 'Comentario creado correctamente'}, HTTP_201_CREATED)


class EvaluarPlanFormacion(CreateAPIView, PlanFormacionMixin):
    """
    PERMITE EVALUAR UN PLAN DE FORMACION INDIVIDUAL
    """
    permission_classes = (IsPlanTutorPermissions,)
    serializer_class = CrearEvaluacionFinalModelSerializer

    def create(self, request, *args, **kwargs):
        plan = self.get_plan()
        etapas_sin_evaluar = EtapaFormacion.objects. \
            filter(Q(evaluacion=None) | Q(evaluacion__aprobadoPor=None), plan_id=plan.pk).exists()
        if plan.evaluation_approved or not plan.is_approved or etapas_sin_evaluar:
            raise CantEvaluateException

        serializer = self.get_serializer(instance=plan.evaluacion, data=request.data)
        serializer.is_valid(raise_exception=True)
        evaluacion = serializer.save()

        if not plan.evaluacion:
            signals.evaluacion_creada.send(evaluacion, plan=plan)
            plan.evaluacion_id = evaluacion.pk
            plan.save()
        else:
            signals.evaluacion_actualizada.send(evaluacion, plan=plan)

        return Response({'detail': 'Plan evaluado correctamente'}, HTTP_200_OK)


class VersionesPlanFormacion(ListAPIView, PlanFormacionMixin):
    """
    PERMITE CARGAR LAS VERSIONES DEL PLAN DE FORMACION INDIVIDUAL
    """
    permission_classes = (IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions,)
    serializer_class = ArchivoModelSerializer

    def get_queryset(self):
        planID = self.get_planID()
        return Archivo.objects.filter(plan_id=planID).order_by('-fecha').all()


class FirmarPlanFormacion(CreateAPIView, PlanFormacionMixin):
    """
    PERMITE APROBAR UN PLAN DE FORMACION INDIVIDUAL SUBIENDO UN ARCHIVO FIRMADO
    """
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
    """
    PERMITE EXPORTAR UN PLAN DE FORMACION A PDF
    """
    permission_classes = [IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions]
    plain_exporter_class = PlainPDFExporter


class ExportarCalendarioPlanFormacionComplemtaria(PlanFormacionExportMixin):
    """
        PERMITE EXPORTAR UN PLAN DE FORMACION A CALENDARIO
    """
    permission_classes = [IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions]
    plain_exporter_class = PlainCalendarExporter


"""
*************************
FORMACION POR ETAPAS
************************
"""


class ListEtapasPlanFormacion(ListAPIView, PlanFormacionMixin):
    """
    PERMITE LISTAR LAS ETAPAS DE UN PLAN DE FORMACION INDIVIDUAL
    """
    permission_classes = [IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions]
    serializer_class = EtapaFormacionModelSerializer

    def get_queryset(self):
        planID = self.get_planID()
        return EtapaFormacion.objects.filter(plan_id=planID).order_by('numero').all()


class RetrieveUpdateEtapaFormacion(RetrieveUpdateAPIView, EtapaFormacionMixin, MultiplePermissionsView):
    """
    PERMITE ACTUALIZAR LOS DATOS DE LA ETAPA DE FORMACION COMPLEMENTARIA Y OBTENER LA MISMA
    """
    put_permission_classes = [IsPlanTutorPermissions]
    get_permission_classes = [IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions]
    serializer_class = EtapaFormacionModelSerializer

    http_method_names = ('get', 'put')

    def get_object(self):
        return self.get_etapa()

    def update(self, request, *args, **kwargs):
        self.can_manage_etapa()

        instance = self.get_object()
        serializer = UpdateEtapaFormacionSerializer(instance, data=request.data)
        serializer.is_valid(True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, HTTP_200_OK)


class EvaluarEtapaFormacion(CreateAPIView, EtapaFormacionMixin):
    """
    PERMITE EVALUAR LA ETAPA DE FORMACION
    """
    permission_classes = (IsPlanTutorPermissions,)
    serializer_class = CrearEvaluacionFormacionModelSerializer

    def get_object(self):
        return self.get_etapa()

    def create(self, request, *args, **kwargs):
        etapa = self.get_object()
        plan = self.get_plan()
        etapas_sin_evaluar = plan.etapas.filter(Q(etapaformacion__evaluacion=None) |
                                                Q(etapaformacion__evaluacion__aprobadoPor=None),
                                                etapaformacion__numero__lt=etapa.numero).count()
        if etapa.evaluation_approved or not plan.is_approved and etapas_sin_evaluar:
            raise CantEvaluateException

        serializer = self.get_serializer(instance=etapa.evaluacion, data=request.data)
        serializer.is_valid(raise_exception=True)
        evaluacion = serializer.save()
        if not etapa.evaluacion:
            etapa.evaluacion_id = evaluacion.pk
            etapa.save()
            signals.evaluacion_creada.send(evaluacion, plan=plan, etapa=etapa)
        else:
            signals.evaluacion_actualizada.send(evaluacion, plan=plan, etapa=etapa)

        return Response({'detail': 'Etapa evaluada correctamente'}, HTTP_200_OK)


"""
****************
EVALUACIONES
****************
"""


class ListRetrieveEvaluacionesArea(ReadOnlyModelViewSet):
    permission_classes = (IsJefeArea,)
    serializer_class = EvaluacionModelSerializer

    def get_queryset(self):
        areaID = self.request.user.area_id
        query = Evaluacion.objects.filter(
            Q(evaluacionfinal__planformacion__aprobadoPor__area_id=areaID) |
            Q(evaluacionformacion__etapaformacion__plan__aprobadoPor__area_id=areaID)) \
            .order_by('-id').all()
        return query


class AprobarEvaluacion(CreateAPIView, EtapaFormacionMixin):
    """
    PERMITE ACEPTAR UNA EVALUACION, UNA VEZ ACEPTADA SE EJECUTA LA ACCION QUE ESTA CONTENGA
    """
    permission_classes = (IsPlanJefeArea,)

    def create(self, request, evaluacionID, *args, **kwargs):
        evaluacion = get_object_or_404(Evaluacion, pk=evaluacionID)

        if evaluacion.aprobadoPor_id is not None:
            raise EvaluacionAlreadyApproved

        evaluacion.aprobadoPor = request.user
        evaluacion.save()
        plan = self.get_plan()

        evaluacion = evaluacion.evaluacionformacion if hasattr(evaluacion,
                                                               'evaluacionformacion') else evaluacion.evaluacionfinal

        signals.evaluacion_aprobada.send(evaluacion, plan=plan)
        return Response({'detail': 'Evaluacion aprobada correctamente'}, HTTP_200_OK)


"""
****************
TAREA DE FORMACION
****************
"""


class ListCreateActividadFormacion(ListCreateAPIView, MultiplePermissionsView, ActividadFormacionMixin):
    """
    PARA CREAR ADICIONAR TAREAS A LAS ETAPAS EL PLAN NO DEBE ESTAR APROBADO NI LA ETAPA DEBE ESTAR EVALUADA
    """
    get_permission_classes = [IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions]
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
                                             ActividadFormacionMixin):
    """
    PERMITE GESTIONAR LAS TAREAS DE FORMACION INDIVIDUAL
    """
    get_permission_classes = [IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions]
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

        signals.actividad_revisada.send(actividad, plan=self.get_plan())
        return Response({'detail': 'Actividad actualizada correctamente'})

    def destroy(self, request, *args, **kwargs):
        self.can_manage_actividad()
        super(RetrieveUpdateDeleteActividadFormacion, self).destroy(request, *args, **kwargs)
        return Response({'detail': 'Actividad borrada correctamente'})


class ListCreateSubActividadFormacion(ListCreateAPIView, MultiplePermissionsView, ActividadFormacionMixin):
    """
    PERMITE CREAR Y LISTAR LAS SUBTAREAS DADO UNA TAREA PADRE
    """
    get_permission_classes = [IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions]
    post_permission_classes = [IsPlanJovenPermissions | IsPlanTutorPermissions]
    serializer_class = ActividadFormacionModelSerializer

    def get_queryset(self):
        actividad = self.get_actividad()
        return ActividadFormacion.objects.filter(actividadPadre=actividad).all()

    def create(self, request, *args, **kwargs):
        self.can_manage_subactividades()
        actividad = self.get_actividad()
        serializer = CreateUpdateActividadFormacionSerializer(data=request.data)
        serializer.is_valid(True)
        serializer.save(etapa_id=actividad.etapa_id, actividadPadre_id=actividad.pk)
        return Response({'detail': 'Actividad creada correctamente'})


class SolicitarRevisionActividadFormacion(CreateAPIView, ActividadFormacionMixin):
    """
    PERMITE SOLICITAR LA REVISION DE UNA TAREA AL TUTOR
    """
    permission_classes = (IsPlanJovenPermissions,)

    def create(self, request, *args, **kwargs):
        self.can_change_actividad_status()
        actividad = self.get_actividad()
        actividad.estado = actividad.Estado.ESPERA
        actividad.fechaCumplimiento = now()
        actividad.save()

        actividad_revision_solicitada.send(actividad, plan=self.get_plan())

        return Response({'detail': 'Solicitud de revision enviada para la actividad'})


class ListCreateActividadFormacionCommets(ListCreateAPIView, ActividadFormacionMixin):
    """
    LOS COMENTARIOS A LAS ACTIVIDADES SE HACE UNA VEZ APROBADO EL PLAN
    """
    permission_classes = (IsPlanJovenPermissions | IsPlanTutorOrJefeAreaPermissions,)
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

        signals.actividad_comentada.send(comentario, plan=self.get_plan(), actividad=self.get_actividad())

        return Response({'detail': 'Comentario creado correctamente'}, HTTP_201_CREATED)


class ActividadFormacionUploadFile(CreateAPIView, ActividadFormacionMixin):
    """
    PERMITE SUBIR UN ARCHIVO A LA ACTIVIDAD, ESTO ES UTIL PORQUE PUEDES ENTREGAR TAREAS MEDIANTE ESTA OPCION
    """
    permission_classes = [IsPlanJovenPermissions | IsPlanTutorPermissions]
    serializer_class = SubirArchivoActividad

    def create(self, request, *args, **kwargs):
        self.can_upload_file()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        serializer.save(actividad_id=self.get_actividadID(), plan_id=self.get_planID())

        return Response({'detail': 'Archivo subido correctamente'}, HTTP_201_CREATED)


class RetrieveDeleteArchive(RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    PERMITE GESTIONAR LOS ARCHIVOS SUBIDOS AL SISTEMA
    """
    serializer_class = ArchivoModelSerializer
    queryset = Archivo.objects.all()

    def destroy(self, request, *args, **kwargs):
        super(RetrieveDeleteArchive, self).destroy(request, *args, **kwargs)
        return Response({'detail': 'Archivo borrado correctamente'})


class PropuestaMovimientoModelViewset(ModelViewSet, MultiplePermissionsView):
    post_permission_classes = [IsJefeArea]
    delete_permission_classes = [IsJefeArea]
    put_permission_classes = [IsJefeArea]
    patch_permission_classes = [IsJefeArea]

    queryset = PropuestaMovimiento.objects.all()
    serializer_class = PropuestaMovimientoModelSerializer

    def create(self, request, *args, **kwargs):
        super(PropuestaMovimientoModelViewset, self).create(request, *args, **kwargs)
        return Response({'detail': 'Propuesta de movimiento creada correctamente'}, HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super(PropuestaMovimientoModelViewset, self).destroy(request, *args, **kwargs)
        return Response({'detail': 'Propuesta de movimiento borrada correctamente'}, HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        super(PropuestaMovimientoModelViewset, self).update(request, *args, **kwargs)
        return Response({'detail': 'Propuesta de movimiento actualizada correctamente'}, HTTP_200_OK)
