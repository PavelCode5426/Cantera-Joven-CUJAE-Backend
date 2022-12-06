from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from core.base.generics import MultiplePermissionsView
from core.base.models.modelosPlanificacionFormacion import PlanFormacionComplementaria, EtapaFormacion
from core.base.models.modelosSimple import Area
from core.base.permissions import IsJefeArea, IsTutor
from core.configuracion.helpers import configValue
from core.formacion_complementaria.base.permissions import IsSameGraduateWhoRequestPermissions, \
    IsSameTutorWhoRequestPermissions
from core.formacion_complementaria.planificacion.exceptions import GraduateHavePlan, CantUpdatePlanAfterApproved, \
    CantEvaluateException, CantApproveException, ResourceNeedEvaluationException
from core.formacion_complementaria.planificacion.permissions import IsGraduateTutorOrJefeAreaPermissions, \
    IsGraduateTutorPermissions, IsPlanGraduatePermissions, IsPlanTutorOrJefeAreaPermissions, IsPlanTutorPermissions, \
    IsPlanJefeArea
from core.formacion_complementaria.planificacion.serializers import PlanFormacionComplementariaModelSerializer, \
    EtapaFormacionModelSerializer, UpdateEtapaFormacionSerializer, CrearEvaluacionModelSerializer
from custom.authentication.models import DirectoryUser


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
            for i in range(1, configValue('etapas_plan_formacion_complementaria') + 1):
                EtapaFormacion(numero=i, plan=plan).save()

            plan.refresh_from_db()
            serializer = self.get_serializer(plan)
            # TODO REVISAR QUE FALTAN ATRIBUTOS DE LA ETAPA
            return Response(serializer.data, HTTP_201_CREATED)
        except IntegrityError as e:
            print(e)
            PlanFormacionComplementaria.objects.filter(graduado_id=graduadoID).delete()
            raise GraduateHavePlan


class ListEtapasPlanFormacionComplementaria(ListAPIView):
    permission_classes = [IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions]
    serializer_class = EtapaFormacionModelSerializer

    def get_queryset(self):
        planID = self.kwargs.get('planID')
        return EtapaFormacion.objects.filter(plan_id=planID).all()


class RetrieveUpdateEtapaFormacion(RetrieveUpdateAPIView, MultiplePermissionsView):
    patch_permission_classes = [IsPlanTutorPermissions]
    get_permission_classes = [IsPlanGraduatePermissions | IsPlanTutorOrJefeAreaPermissions]
    serializer_class = EtapaFormacionModelSerializer

    http_method_names = ('get', 'put')

    def get_object(self):
        return get_object_or_404(EtapaFormacion, pk=self.kwargs['etapaID'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.plan.is_approved:
            raise CantUpdatePlanAfterApproved

        serializer = UpdateEtapaFormacionSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class EvaluarEtapaFormacion(CreateAPIView):
    # TODO LISTAR PLANES PENDIENTES POR EVALUAR Y APROBAR LA EVALUACION POR EL PLAN
    permission_classes = (IsPlanTutorPermissions,)
    serializer_class = CrearEvaluacionModelSerializer

    def create(self, request, etapaID, *args, **kwargs):
        etapa = get_object_or_404(EtapaFormacion, pk=etapaID)
        plan = get_object_or_404(PlanFormacionComplementaria, pk=etapa.plan_id)
        if etapa.evaluation_approved or not plan.is_approved:
            raise CantEvaluateException

        serializer = CrearEvaluacionModelSerializer(instance=etapa.evaluacion, data=request.data)
        serializer.is_valid(raise_exception=True)
        etapa.evaluacion = serializer.save()
        etapa.save()
        return Response({'detail': 'Etapa evaluada correctamente'}, HTTP_200_OK)


class AprobarEvaluacionEtapaFormacion(CreateAPIView):
    # TODO PENSAR SI ES NECESARIO APROBAR LA EVALUACION O APROBAR LA EVALUACION DE LA ETAPA
    permission_classes = (IsPlanJefeArea)

    def create(self, request, etapaID, *args, **kwargs):
        etapa = get_object_or_404(EtapaFormacion, pk=etapaID)

        if not etapa.evaluacion:
            raise ResourceNeedEvaluationException
        elif etapa.evaluation_approved:
            raise CantApproveException

        etapa.evaluacion.aprobadoPor = request.user
        return Response({'detail', 'Evaluacion aprobada correctamente'}, HTTP_200_OK)
