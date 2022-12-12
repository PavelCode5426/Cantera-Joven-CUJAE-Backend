from .signals import plan_creado


def plan_listener(*args, **kwargs):
    pass


plan_creado.connect(plan_listener)
