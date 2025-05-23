"""
URL configuration for smartskill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import debug_toolbar
from decouple import config
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

APP_NAME_API = config("APP_NAME_API", default="default_app_name")
API_VERSION = config("API_VERSION", default="v1")


def redirect_to_swagger(request):
    return redirect("schema-swagger-ui")


urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{APP_NAME_API}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="schema-swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "", redirect_to_swagger
    ),  # Ensure this is after all other paths to avoid conflicts
    path(f"{APP_NAME_API}/v{API_VERSION}/users/", include("apps.user.urls")),
    path(f"{APP_NAME_API}/v{API_VERSION}/skills/", include("apps.skills.urls")),
    path(
        f"{APP_NAME_API}/v{API_VERSION}/experiences/", include("apps.experiences.urls")
    ),
    path(
        f"{APP_NAME_API}/v{API_VERSION}/qualifications/",
        include("apps.qualifications.urls"),
    ),
    path(
        f"{APP_NAME_API}/v{API_VERSION}/projects/",
        include("apps.projects.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
