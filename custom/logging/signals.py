from django.contrib.admin.options import get_content_type_for_model
from .tracker import modelTracker
from django.contrib.admin.models import *
from crum import get_current_request

EXCLUDE_URLS = ['/admin']

def post_delete_action_logging(sender, instance, **kwargs):
    request = get_current_request()
    is_in = False

    if request:
        path_url:str = request.path
        ite = iter(EXCLUDE_URLS)

        try:
            item = next(ite)
            while item and not is_in:
                if item.startswith(path_url):
                    is_in = True
                item = next(ite)
        except StopIteration:
            pass

    if not is_in and modelTracker.is_register(instance):
        user = request.user if request else None
        if user:
            LogEntry.objects.log_action(
                user_id=user.pk,
                content_type_id=get_content_type_for_model(instance).pk,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=DELETION,
            )

def post_save_action_logging(sender,instance,created,*args,**kwargs):
    request = get_current_request()
    is_in = False

    if request:
        path_url: str = request.path
        ite = iter(EXCLUDE_URLS)

        try:
            item = next(ite)
            while item and not is_in:
                if item.startswith(path_url):
                    is_in = True
                item = next(ite)
        except StopIteration:
            pass

    if not is_in and modelTracker.is_register(instance):
        action = ADDITION if created else CHANGE

        user = request.user if request else None
        if user:
            LogEntry.objects.log_action(
                user_id=user.pk,
                content_type_id=get_content_type_for_model(instance).pk,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=action,
            )