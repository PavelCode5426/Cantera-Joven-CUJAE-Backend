from notifications.signals import notify

from custom.authentication.models import DirectoryUser

for user in DirectoryUser.objects.all():
    for number in range(0, 10):
        sender = DirectoryUser.objects.order_by('?').first()
        texto = "Texto de prueba por " + sender.first_name
        notify.send(sender, recipient=user, verb=texto)
