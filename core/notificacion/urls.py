from django.urls import path
from . import views
from notifications import views as v
# Create your views here.
app_name = 'Notificacion'
app_prefix = 'notificacion/'

#Notifications.url
urlpatterns = [
    path('marcar-todos-como-leido',views.MarkAllAsRead.as_view()),
    path('marcar-como-leido/<int:slug>', views.MarkAsRead.as_view()),
    path('marcar-como-no-leido/<int:slug>',views.MarkAsUnread.as_view()),
    path('<int:slug>', views.DeleteNotification.as_view()),

    #En vivo
    path('cantidad-sin-leer', views.LiveUnreadCount.as_view()),
    path('sin-leer', views.LiveUnreadList.as_view()),
    path('', views.ListSendNotifications.as_view()),
    path('', views.ListSendNotifications.as_view()),
    path('masiva', views.SendMasiveNotifications.as_view()),
]