from django.urls import path
from .views import CustomTokenObtainPairView, UserDetailView, UserListCreateView
from rest_framework_simplejwt.views import TokenRefreshView
common_actions = {
    "get": "list",
    "post": "create",
}

user_paths = [
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    path('token/create', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = user_paths