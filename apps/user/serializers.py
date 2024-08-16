from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return data

