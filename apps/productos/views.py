# apps/productos/views.py

from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from apps.productos.models import Producto
from apps.productos.serializers import ProductoSerializer


class ProductoPagination(PageNumberPagination):
    """Paginación para productos"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos.
    - GET: Público (ver productos disponibles)
    - POST/PUT/PATCH/DELETE: Solo admin
    """
    serializer_class = ProductoSerializer
    pagination_class = ProductoPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'codigo', 'categoria', 'descripcion']
    ordering_fields = ['precio', 'nombre', 'created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Permisos según la acción"""
        if self.action == 'list' or self.action == 'retrieve':
            # GET: Público, solo productos activos
            return [permissions.AllowAny()]
        # POST, PUT, PATCH, DELETE: Solo admin
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        """Filtra productos según permisos"""
        if self.request.user and self.request.user.is_staff:
            # Admins ven todos los productos
            return Producto.objects.all()
        # Público solo ve productos activos con stock > 0
        queryset = Producto.objects.filter(activo=True, stock__gt=0)
        
        # Filtro opcional por categoría
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        # Filtro opcional por rango de precio
        precio_min = self.request.query_params.get('precio_min', None)
        precio_max = self.request.query_params.get('precio_max', None)
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)
        
        return queryset

