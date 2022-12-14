from __future__ import annotations

from annoying.functions import get_object_or_None

from core.base.models.modelosUsuario import Estudiante, Graduado
from custom.authentication.models import DirectoryUser


def user_is_student(user: DirectoryUser) -> Estudiante | None:
    return get_object_or_None(Estudiante, pk=user.pk)


def user_is_gradute(user: DirectoryUser) -> Graduado | None:
    return get_object_or_None(Graduado, pk=user.pk)


def user_student_or_graduate(user: DirectoryUser) -> (Estudiante | Graduado, bool):
    graduate = user_is_gradute(user)
    if graduate:
        return graduate, False
    student = user_is_student(user)
    return student, student is not None
