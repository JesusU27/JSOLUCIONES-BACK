# apps/clientes/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class Cliente(AbstractUser):
    """
    Modelo de Cliente que extiende AbstractUser.
    Representa a los usuarios/clientes del sistema que pueden comprar productos.
    """
    
    # Override email para que sea unique (requerido cuando es USERNAME_FIELD)
    email = models.EmailField(unique=True)
    
    # Campos adicionales más allá de AbstractUser
    documento = models.CharField(
        max_length=20, 
        unique=True,
        help_text="DNI, RUC o documento de identidad"
    )
    telefono = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Teléfono de contacto"
    )
    direccion = models.TextField(
        blank=True, 
        null=True,
        help_text="Dirección de entrega"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Configuración de autenticación
    USERNAME_FIELD = 'email'  # Login con email en lugar de username
    REQUIRED_FIELDS = ['username', 'documento', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    @property
    def total_compras(self):
        """Retorna el número total de compras del cliente"""
        return self.compras.filter(estado='COMPLETADA').count()
    
    @property
    def total_gastado(self):
        """Retorna el monto total gastado por el cliente"""
        from django.db.models import Sum
        total = self.compras.filter(estado='COMPLETADA').aggregate(
            total=Sum('total')
        )['total']
        return total or 0