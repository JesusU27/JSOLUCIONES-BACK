# apps/productos/models.py

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Producto(models.Model):
    """
    Modelo de Producto.
    Representa los items disponibles para la venta.
    """
    
    codigo = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Código único del producto (SKU)"
    )
    nombre = models.CharField(
        max_length=200,
        help_text="Nombre del producto"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True,
        help_text="Descripción detallada del producto"
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Precio unitario del producto"
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Cantidad disponible en inventario"
    )
    categoria = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Categoría del producto"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Si el producto está disponible para la venta"
    )
    imagen_url = models.URLField(
        blank=True, 
        null=True,
        help_text="URL de la imagen del producto"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['categoria']),
            models.Index(fields=['activo']),
        ]
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def disponible(self):
        """Verifica si el producto está disponible para la venta"""
        return self.activo and self.stock > 0
    
    def descontar_stock(self, cantidad):
        """Descuenta stock del producto"""
        if cantidad > self.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock}")
        self.stock -= cantidad
        self.save(update_fields=['stock', 'updated_at'])
    
    def aumentar_stock(self, cantidad):
        """Aumenta el stock del producto"""
        self.stock += cantidad
        self.save(update_fields=['stock', 'updated_at'])