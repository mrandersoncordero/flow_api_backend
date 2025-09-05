from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from petitions.models import Notification
from petitions.serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework import status

class NotificationListView(ListAPIView):
    """Lista de notificaciones del usuario autenticado."""
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtra notificaciones según el grupo del usuario."""

        user = self.request.user

        # if user.groups.filter(name="Admin").exists():
        #     return Notification.objects.all()  # 🔥 Admins ven TODO

        return Notification.objects.filter(recipient=user)  # 🔥 Managers y Clients ven solo las suyas
    
class NotificationMarkAsReadView(UpdateAPIView):
    """Marca una notificación como leída."""
    
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.status = "read"
        notification.save()
        return Response({"message": "Notificación marcada como leída."}, status=status.HTTP_200_OK)
