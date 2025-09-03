"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="DuPoon API",
        default_version="v1",
        description="API documentation for DuPoon",
        contact=openapi.Contact(email="swpark.biz@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Swagger UI
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # ReDoc UI
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Admin interface
    path("admin/", admin.site.urls),
    # User Authentication
    path("accounts/", include("django.contrib.auth.urls")),
    # API authentication
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # Include app URLs
    path("", include("apps.core.urls")),
    path("stock/", include("apps.stock.urls", namespace="stock")),
    path("backtest/", include("apps.backtest.urls", namespace="backtest")),
    path("strategy/", include("apps.strategy.urls", namespace="strategy")),
    # API endpoints
    path("api/stock/", include("apps.stock.api_urls")),
    path("api/backtest/", include("apps.backtest.api_urls")),
    path("api/strategy/", include("apps.strategy.api_urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
