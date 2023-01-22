from ..models.modelosUsuario import Graduado

fake_data_aval = {
    'usuario': lambda x: Graduado.objects.filter(aval=None).order_by('?').first()
}

# seeder.add_entity(Aval, 50, fake_data_aval)
# seeder.add_entity(TutoresAsignados, 50)

# seeder.add_entity(Plan, 100)
# seeder.add_entity(Etapa, 100)
# seeder.add_entity(ActividadColectiva, 100)
# seeder.add_entity(UbicacionLaboralAdelantada, 1000, {
#     'area': lambda x: Area.objects.order_by('?').first()
# })

# seeder.add_entity(PlanFormacion, 100)
# seeder.add_entity(EtapaFormacion, 100)
# seeder.add_entity(ActividadFormacion, 100)
