from django.dispatch import Signal

plan_creado = Signal()
plan_revision_solicitada = Signal()
plan_aprobado = Signal()
plan_rechazado = Signal()
plan_comentado = Signal()

evaluacion_creada = Signal()
evaluacion_actualizada = Signal()
evaluacion_aprobada = Signal()

actividad_revisada = Signal()
actividad_revision_solicitada = Signal()
actividad_comentada = Signal()
