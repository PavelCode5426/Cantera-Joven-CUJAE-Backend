from rest_framework import permissions


#roles = [
#    {'nombre':'Tutor'},
 #   {'nombre':'Jefe de Area'},
  #  {'nombre':'Director Recursos Humanos'},
   # {'nombre':'Vicerrector'},
    #{'nombre':'Estudiante'},
    #{'nombre':'Graduado'},
    #{'nombre':'Posible Graduado'},
#]

class IsTutor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Tutor").exists():
            return True


class IsJefeArea(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Jefe de Area").exists():
            return True


class IsDirectorRH(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Director Recursos Humanos").exists():
            return True


class IsVicerrector(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Vicerrector").exists():
            return True


class IsEstudiante(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Estudiante").exists():
            return True


class IsPosibleGraduado(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Posible Graduado").exists():
            return True


class IsGraduado(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Graduado").exists():
            return True


