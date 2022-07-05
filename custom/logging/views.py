from rest_framework.generics import ListAPIView
from .serializers import LogEntrySerializer

class ListUserLogEntries(ListAPIView):
    serializer_class = LogEntrySerializer
    def get_queryset(self):
        current_user = self.request.user
        return current_user.logentry_set.all()
