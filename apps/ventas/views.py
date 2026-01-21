# apps/ventas/views.py

from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from apps.ventas.models import Venta, DetalleVenta
from apps.ventas.serializers import (
    VentaSerializer, VentaCrearSerializer, VentaListaSerializer, DetalleVentaSerializer,
    VentaClienteSerializer
)


class VentaAdminViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para que admins vean todas las ventas"""
    queryset = Venta.objects.all()
    serializer_class = VentaListaSerializer
    permission_classes = [permissions.IsAdminUser]


class VentaCrearViewSet(generics.CreateAPIView):
    """Vista para que clientes autenticados creen ventas"""
    serializer_class = VentaCrearSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Crear una nueva venta con detalles"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            venta = serializer.save()
            # Retornar los datos completos de la venta creada
            output_serializer = VentaSerializer(venta)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VentaClienteViewSet(viewsets.ViewSet):
    """ViewSet para que clientes vean sus propias compras"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VentaClienteSerializer
    
    @action(detail=False, methods=['get'])
    def mis_compras(self, request):
        """Obtener historial de compras del cliente autenticado"""
        ventas = Venta.objects.filter(cliente=request.user)
        serializer = VentaClienteSerializer(ventas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def resumen(self, request):
        """Obtener resumen de todas las ventas (solo admin)"""
        ventas = Venta.objects.all()
        total_ventas = ventas.count()
        monto_total = sum(v.total for v in ventas)
        
        return Response({
            'total_ventas': total_ventas,
            'monto_total': float(monto_total),
            'promedio_venta': float(monto_total / total_ventas) if total_ventas > 0 else 0,
            'ultima_venta': ventas.first().fecha_venta if total_ventas > 0 else None
        })

