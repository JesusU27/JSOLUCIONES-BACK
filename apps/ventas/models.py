# apps/ventas/models.py

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.clientes.models import Cliente
from apps.productos.models import Producto


class EstadoVentaChoices(models.TextChoices):
    """Opciones de estado para una venta"""
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    COMPLETADA = 'COMPLETADA', 'Completada'
    CANCELADA = 'CANCELADA', 'Cancelada'


class Venta(models.Model):
    """
    Modelo de Venta.
    Representa una transacción de compra realizada por un cliente.
    """
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='compras',
        help_text="Cliente que realizó la compra"
    )
    fecha_venta = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de la venta"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Monto total de la venta"
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoVentaChoices.choices,
        default=EstadoVentaChoices.COMPLETADA,
        help_text="Estado actual de la venta"
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        help_text="Observaciones o notas adicionales"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha_venta']
        indexes = [
            models.Index(fields=['cliente', 'fecha_venta']),
            models.Index(fields=['estado']),
            models.Index(fields=['-fecha_venta']),
        ]
    
    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.get_full_name()} - ${self.total}"
    
    def calcular_total(self):
        """Calcula el total de la venta sumando los subtotales de los detalles"""
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
        self.save(update_fields=['total', 'updated_at'])
        return total


class DetalleVenta(models.Model):
    """
    Modelo de DetalleVenta.
    Representa cada producto individual dentro de una venta.
    """
    
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles',
        help_text="Venta a la que pertenece este detalle"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        help_text="Producto vendido"
    )
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Cantidad de unidades vendidas"
    )
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Precio unitario al momento de la venta"
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Subtotal (cantidad × precio_unitario)"
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'detalle_ventas'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'
        ordering = ['id']
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} - ${self.subtotal}"
    
    def save(self, *args, **kwargs):
        """Calcula el subtotal antes de guardar"""
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)