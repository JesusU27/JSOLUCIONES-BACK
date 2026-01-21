# apps/productos/serializers.py

from rest_framework import serializers
from apps.productos.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    """Serializador para productos"""
    
    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'nombre', 'descripcion', 'precio', 'stock', 
                  'categoria', 'activo', 'imagen_url', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_precio(self, value):
        """Valida que el precio sea mayor a 0"""
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor a 0.')
        return value
    
    def validate_stock(self, value):
        """Valida que el stock no sea negativo"""
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return value
