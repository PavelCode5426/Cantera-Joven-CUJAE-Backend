from crum import get_current_user

from custom.authentication.models import DirectoryUser


def get_tutor(pk, **kwargs):
    result = None
    try:
        result = DirectoryUser.objects.get(pk=pk, graduado=None, posiblegraduado=None, estudiante=None, **kwargs)
    except DirectoryUser.DoesNotExist:
        result = None
    return result


def get_all_tutors():
    return DirectoryUser.objects.filter(graduado=None, posiblegraduado=None, estudiante=None).all()


def get_all_tutors_from_area(area):
    return DirectoryUser.objects.filter(graduado=None, posiblegraduado=None, estudiante=None, area=area).all()


def get_all_tutors_from_current_area():
    user = get_current_user()
    area = None if not hasattr(user, 'area') else user.area
    return get_all_tutors_from_area(area)
