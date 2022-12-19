from notifications.signals import notify


def mass_notify(users: list, from_user, text, data, *args, **kwargs):
    for user in users:
        notify.send(from_user, recipient=user, verb=text, data=data, *args, **kwargs)
