from custom.authentication.models import DirectoryUser

def get_tutor(pk,**kwargs):
    result = None
    try:
        result = DirectoryUser.objects.get(pk=pk,graduado=None,posiblegraduado=None,estudiante=None,**kwargs)
    except DirectoryUser.DoesNotExist:
        result = None
    return result