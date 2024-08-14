from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.utils.paginations import DefaultPagination
from user.serializers import UserSerializer
from .models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["email","first_name","last_name"]
    pagination_class = DefaultPagination

    def create(self, request, *args, **kwargs):
        # Extract the password from the request data
        password = request.data.get('password', None)

        # Use the serializer to validate the rest of the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Set and hash the password if it was provided
        if password:
            user = User(**serializer.validated_data)
            user.set_password(password)
        else:
            user = User(**serializer.validated_data)

        # Save the user to the database
        user.save()

        # Return the serialized user data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # Get the user instance to be updated
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Extract the password from the request data
        password = request.data.get('password', None)

        # Use the serializer to validate the rest of the data
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Save the user instance without saving it to the database yet
        user = serializer.save(commit=False)

        # Set and hash the password if it was provided
        if password:
            user.set_password(password)

        # Save the user to the database
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
