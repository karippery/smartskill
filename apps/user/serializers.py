from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.models import PasswordResetToken, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["groups", "user_permissions"]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user_id"] = self.user.id
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Normalize the email by lowercasing it, assuming case-insensitive emails
        email = value.lower().strip()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "No account is associated with this email address."
            )
        return email


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        if not PasswordResetToken.objects.filter(token=value).exists():
            raise serializers.ValidationError("Invalid or expired token.")
        return value

    def validate(self, attrs):
        token = attrs.get("token")
        reset_token = PasswordResetToken.objects.get(token=token)
        if not reset_token.is_valid():
            raise serializers.ValidationError("This password reset link has expired.")
        return attrs

    def save(self, **kwargs):
        token = self.validated_data.get("token")
        new_password = self.validated_data.get("new_password")
        reset_token = PasswordResetToken.objects.get(token=token)
        user = reset_token.user
        user.set_password(new_password)
        user.save()
        reset_token.delete()  # Invalidate the token after successful reset
        return user
