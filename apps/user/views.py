from smtplib import SMTPAuthenticationError
import uuid
from django.urls import NoReverseMatch, reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from apps.user.models import PasswordResetToken, User
from apps.user.serializers import CustomTokenObtainPairSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, UserSerializer
from core.utils.paginations import DefaultPagination
from rest_framework import viewsets, status
from django.template.loader import render_to_string
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from django.core.mail import send_mail

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["email", "first_name", "last_name"]
    pagination_class = DefaultPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = request.data.get('password', None)
        if password:
            user.set_password(password)
            user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password', None)
        if password:
            user.set_password(password)
            user.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PasswordResetRequestView(generics.GenericAPIView):

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        token = uuid.uuid4().hex  # Generate a random token
        PasswordResetToken.objects.create(user=user, token=token)

        try:
            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', args=[token])
            )
        except NoReverseMatch as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        subject = "Password Reset Requested"
        message = render_to_string('emails/password_reset_email.html', {
            'reset_link': reset_link,
            'user': user
        })

        try:
            send_mail(subject, message, None, [user.email])
        except SMTPAuthenticationError as e:
            return Response({"detail": "SMTP Authentication Error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"detail": "An error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "A password reset link has been sent to your email."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your password has been reset successfully."}, status=status.HTTP_200_OK)