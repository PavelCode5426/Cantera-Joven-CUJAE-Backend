__posiblesGraduados = [
    {'id':234,'email':'estudiante_101@gmail.com','username':'hdiego','first_name':'Diego','last_name':'Hernanedez','direccion':'Playa 1500',
     'lugarProcedencia':'Universidad de Ciencias Informaticas'},
    {'id':187,'email':'estudiante100@gmail.com','username':'eliii','first_name':'Eli','last_name':'Garcia','direccion':'Ave 51 Calle 90',
     'lugarProcedencia':'Universidad de la Habana'},
    {'id':777,'email':'estudiante000@gmail.com','username':'carlos10','first_name':'Carlos','last_name':'Garcia','direccion':'Ave 51 Calle 88A',
     'lugarProcedencia':'Universidad Pedagogica de la Habana'},
    {'id':787,'email':'estudiante9@gmail.com','username':'lia','first_name':'Lia','last_name':'Garcia','direccion':'Ave 1era #100',
     'lugarProcedencia':'Universidad Pedagogica de la Habana'},
    {'id':191,'email':'estudiante8@gmail.com','username':'amivilla','first_name':'Amy','last_name':'Villa','direccion':'La Habana 8976',
     'lugarProcedencia':'Universidad Pedagogica de la Habana'},
]

def obtenerPosibleGraduado(id):
    from . import obtenerPorID
    return obtenerPorID(__posiblesGraduados, id)


def obtenerPosibleGraduados(listIDs=[]):
    from . import obtenerPorIDs
    return obtenerPorIDs(__posiblesGraduados, listIDs)


