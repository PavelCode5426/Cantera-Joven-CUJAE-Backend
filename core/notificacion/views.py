from rest_framework.generics import CreateAPIView, get_object_or_404, DestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from swapper import load_model

from core.notificacion.serializers import EnviarNotificacionSerializer, EnviarNotificacionMasivaSerializer
from .serializers import NotificationSerializer

Notification = load_model('notifications', 'Notification')


class ResultMessage:
    result_message: str


class MarkAs(CreateAPIView, ResultMessage):

    def dispatch(self, request, *args, **kwargs):
        if not self.result_message:
            raise NotImplementedError('Se necesita un mensaje de retorno')
        return super().dispatch(request, *args, **kwargs)

    def mark_as(self, *args, **kwargs) -> None:
        raise NotImplementedError('Se necesita implementar el metodo')

    def create(self, request, *args, **kwargs):
        self.mark_as(*args, **kwargs)
        return Response({'detail': self.result_message}, HTTP_200_OK)


class MarkAllAsRead(MarkAs):
    result_message = 'Todas las notificaciones marcadas como leidas'

    def mark_as(self, *args, **kwargs) -> None:
        self.request.user.notifications.mark_all_as_read()


class MarkAsRead(MarkAs):
    result_message = 'Notificacion marcada como leida'

    def mark_as(self, *args, **kwargs):
        notification_id = kwargs['slug']

        notification = get_object_or_404(
            Notification, recipient=self.request.user, id=notification_id)
        notification.mark_as_read()


class MarkAsUnread(MarkAs):
    result_message = 'Notificacion marcada como no leida'

    def mark_as(self, *args, **kwargs):
        notification_id = kwargs['slug']

        notification = get_object_or_404(
            Notification, recipient=self.request.user, id=notification_id)
        notification.mark_as_unread()


class DeleteNotification(DestroyAPIView, ResultMessage):
    result_message = 'Notificacion borrada correctamente'

    def destroy(self, request, slug, **kwargs):
        notification_id = slug

        notification = get_object_or_404(
            Notification, recipient=self.request.user, id=notification_id)
        notification.delete()
        return Response({'detail': self.result_message}, HTTP_200_OK)


class LiveNotifications(APIView):
    pass


class LiveUnreadCount(LiveNotifications):
    def get(self, *args, **kwargs):
        cantidad = self.request.user.notifications.unread().count()
        return Response({'cantidad_sin_leer': cantidad}, HTTP_200_OK)


class LiveUnreadList(LiveNotifications):
    serializer_class = NotificationSerializer

    def get(self, *args, **kwargs):
        notificaciones = self.request.user.notifications.unread()
        cantidad_no_leida = notificaciones.count()
        notificaciones = NotificationSerializer(notificaciones, many=True).data
        return Response({'cantidad_sin_leer': cantidad_no_leida, 'lista': notificaciones}, HTTP_200_OK)


class ListSendNotifications(LiveNotifications, ListCreateAPIView):
    serializer_class_map = {'GET': NotificationSerializer, 'POST': EnviarNotificacionSerializer}

    def list(self, request, *args, **kwargs):
        notificaciones = request.user.notifications
        cantidad_no_leida = notificaciones.count()
        notificaciones = self.serializer_class_map[request.method](notificaciones, many=True).data
        return Response({'cantidad_total': cantidad_no_leida, 'lista': notificaciones}, HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class_map['POST'](data=data, context={'sender': request.user})
        if not serializer.is_valid():
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        serializer.create(validated_data)
        return Response({'detail': 'Notificacion enviada correctamente'}, HTTP_200_OK)


class SendMasiveNotifications(CreateAPIView):
    serializer_class = EnviarNotificacionMasivaSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data, context={'sender': request.user})
        serializer.is_valid(True)
        serializer.save()
        return Response({'detail': 'Notificacion masiva enviada correctamente'}, HTTP_200_OK)
