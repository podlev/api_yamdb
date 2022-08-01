from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации"""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        """Проверка использования 'me' в качестве username"""
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено.")
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена"""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта /api/v1/users"""

    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
