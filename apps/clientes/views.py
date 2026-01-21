# apps/clientes/views.py

from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from apps.clientes.models import Cliente
from apps.clientes.serializers import (
    ClienteSerializer, RegistroSerializer, LoginSerializer, CambiarPasswordSerializer
)


class RegistroViewSet(generics.CreateAPIView):
    """Vista solo para registrar nuevos clientes"""
    queryset = Cliente.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny]


class ClientesListViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet solo lectura para que admins vean lista de clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAdminUser]


class LoginView(TokenObtainPairView):
    """View para login de clientes con JWT"""
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """Personaliza la respuesta del login para incluir userType"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Obtener el usuario del serializer
        user = serializer.user
        user_type = 'admin' if user.is_staff or user.is_superuser else 'user'
        
        response = super().post(request, *args, **kwargs)
        response.data['userType'] = user_type
        
        return response


class ClienteViewSet(viewsets.GenericViewSet):
    """ViewSet para operaciones de cliente autenticado"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClienteSerializer
    
    @action(detail=False, methods=['get'])
    def perfil(self, request):
        """Obtener perfil del cliente autenticado"""
        serializer = ClienteSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def actualizar_perfil(self, request):
        """Actualizar datos del perfil"""
        serializer = ClienteSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'mensaje': 'Perfil actualizado', 'cliente': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=CambiarPasswordSerializer,
        responses={200: {'description': 'Contraseña actualizada exitosamente'}}
    )
    @action(detail=False, methods=['post'])
    def cambiar_password(self, request):
        """Cambiar contraseña del cliente"""
        serializer = CambiarPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'mensaje': 'Contraseña actualizada exitosamente'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
