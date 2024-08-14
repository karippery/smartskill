from django.urls import path

from user.serializers import CustomTokenObtainPairView

from .views import UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView
common_actions = {
    "get": "list",
    "post": "create",
}

user_paths = [
    path("user/", UserViewSet.as_view(common_actions),
         name="user-list"),
    path("user/<int:pk>/",
         UserViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
         name="user-detail"),

    path('token/create', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = user_paths