# apps/ventas/serializers.py

from rest_framework import serializers
from apps.ventas.models import Venta, DetalleVenta
from apps.productos.models import Producto


class DetalleVentaSimpleSerializer(serializers.Serializer):
    """Serializador simplificado para crear detalles de venta (solo producto y cantidad)"""
    producto = serializers.IntegerField()
    cantidad = serializers.IntegerField()
    
    def validate_cantidad(self, value):
        """Valida que la cantidad sea válida"""
        if value <= 0:
            raise serializers.ValidationError('La cantidad debe ser mayor a 0.')
        return value


class DetalleVentaSerializer(serializers.ModelSerializer):
    """Serializador para mostrar detalles de venta"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario', 
                  'subtotal', 'created_at']
        read_only_fields = ['id', 'subtotal', 'created_at', 'precio_unitario']


class VentaCrearSerializer(serializers.Serializer):
    """Serializador para crear una venta con sus detalles"""
    detalles = DetalleVentaSimpleSerializer(many=True)
    observaciones = serializers.CharField(required=False, allow_blank=True)
    
    def validate_detalles(self, value):
        """Valida que exista al menos un detalle"""
        if not value:
            raise serializers.ValidationError('La venta debe tener al menos un producto.')
        return value
    
    def create(self, validated_data):
        """Crea la venta y sus detalles"""
        detalles_data = validated_data.pop('detalles')
        cliente = self.context['request'].user
        
        # Crear la venta
        venta = Venta.objects.create(
            cliente=cliente,
            observaciones=validated_data.get('observaciones', '')
        )
        
        # Crear los detalles y descontar stock
        for detalle_data in detalles_data:
            producto_id = detalle_data['producto']
            cantidad = detalle_data['cantidad']
            
            # Obtener el producto
            try:
                producto = Producto.objects.get(id=producto_id)
            except Producto.DoesNotExist:
                raise serializers.ValidationError(
                    f'El producto con ID {producto_id} no existe.'
                )
            
            # Validar stock disponible
            if producto.stock < cantidad:
                raise serializers.ValidationError(
                    f'Stock insuficiente para {producto.nombre}. '
                    f'Disponible: {producto.stock}, Solicitado: {cantidad}'
                )
            
            # Crear detalle con el precio actual del producto
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )
            
            # Descontar stock
            producto.stock -= cantidad
            producto.save(update_fields=['stock'])
        
        # Calcular total
        venta.calcular_total()
        
        return venta


class VentaSerializer(serializers.ModelSerializer):
    """Serializador para mostrar detalles de una venta"""
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.get_full_name', read_only=True)
    
    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'cliente_nombre', 'fecha_venta', 'total', 'estado', 
                  'observaciones', 'detalles', 'created_at', 'updated_at']
        read_only_fields = ['id', 'cliente', 'fecha_venta', 'created_at', 'updated_at']


class DetalleVentaClienteSerializer(serializers.ModelSerializer):
    """Serializador para mostrar detalles de compra al cliente"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_descripcion = serializers.CharField(source='producto.descripcion', read_only=True)
    
    class Meta:
        model = DetalleVenta
        fields = ['producto_nombre', 'producto_descripcion', 'cantidad', 'precio_unitario', 'subtotal']
        read_only_fields = fields


class VentaClienteSerializer(serializers.ModelSerializer):
    """Serializador para mostrar ventas/compras del cliente"""
    detalles = DetalleVentaClienteSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        fields = ['id', 'fecha_venta', 'total', 'estado', 'detalles', 'observaciones']
        read_only_fields = fields


class VentaListaSerializer(serializers.ModelSerializer):
    """Serializador simplificado para listar ventas con detalles de productos"""
    cliente_nombre = serializers.CharField(source='cliente.get_full_name', read_only=True)
    cantidad_total = serializers.SerializerMethodField()
    detalles = DetalleVentaClienteSerializer(many=True, read_only=True)
    
    def get_cantidad_total(self, obj):
        """Suma la cantidad total de unidades vendidas"""
        return sum(detalle.cantidad for detalle in obj.detalles.all())
    
    class Meta:
        model = Venta
        fields = ['id', 'cliente_nombre', 'fecha_venta', 'total', 'estado', 
                  'cantidad_total', 'detalles', 'created_at']
        read_only_fields = fields
