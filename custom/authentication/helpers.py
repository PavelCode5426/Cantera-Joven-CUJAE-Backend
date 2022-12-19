from custom.authentication.models import DirectoryUser


def all_user_with_roles(roles: [str]):
    return DirectoryUser.objects.filter(groups__in=roles, is_active=True)
