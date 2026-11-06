from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')

    def partial_update(self, request, *args, **kwargs):
        # Corrección al manual: si no viene contraseña, no se toca.
        # No se copia la contraseña de quien hace la petición.
        if not request.data.get('password'):
            if hasattr(request.data, 'pop'):
                request.data.pop('password', None)
        return super().partial_update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
