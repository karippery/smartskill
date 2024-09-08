from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views import CustomTokenObtainPairView, PasswordResetConfirmView, PasswordResetRequestView, UserDetailView, UserListCreateView
common_actions = {
    "get": "list",
    "post": "create",
}

user_paths = [
    path("", UserListCreateView.as_view(), name="user-list-create"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    path('token/create', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')
]

urlpatterns = user_paths