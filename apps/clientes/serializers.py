# apps/clientes/serializers.py

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.clientes.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    """Serializador para mostrar datos del cliente"""
    total_compras = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cliente
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'documento', 
                  'telefono', 'direccion', 'total_compras', 'created_at']
        read_only_fields = ['id', 'created_at', 'total_compras']


class RegistroSerializer(serializers.ModelSerializer):
    """Serializador para registro de nuevos clientes"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Cliente
        fields = ['email', 'username', 'password', 'password2', 'first_name', 
                  'last_name', 'documento', 'telefono', 'direccion']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'documento': {'required': True},
        }
    
    def validate(self, attrs):
        """Valida que las contraseñas coincidan"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Las contraseñas no coinciden.'
            })
        return attrs
    
    def create(self, validated_data):
        """Crea un nuevo cliente"""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        cliente = Cliente.objects.create_user(**validated_data)
        cliente.set_password(password)
        cliente.save()
        return cliente


class LoginSerializer(TokenObtainPairSerializer):
    """Serializador personalizado para login con email"""
    email = serializers.CharField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')
    
    @classmethod
    def get_token(cls, user):
        """Personaliza el token con información adicional del usuario"""
        token = super().get_token(user)
        token['email'] = user.email
        token['nombre'] = user.get_full_name()
        token['userType'] = 'admin' if user.is_staff or user.is_superuser else 'user'
        return token


class CambiarPasswordSerializer(serializers.Serializer):
    """Serializador para cambiar contraseña"""
    password_actual = serializers.CharField(write_only=True, required=True)
    password_nueva = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_nueva2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs['password_nueva'] != attrs['password_nueva2']:
            raise serializers.ValidationError({
                'password_nueva': 'Las nuevas contraseñas no coinciden.'
            })
        return attrs
    
    def validate_password_actual(self, value):
        """Valida que la contraseña actual sea correcta"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Contraseña actual incorrecta.')
        return value
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['password_nueva'])
        user.save()
        return user
