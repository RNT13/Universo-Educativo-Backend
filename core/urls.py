from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


def api_root(request):
    return JsonResponse(
        {
            "status": "ok",
            "message": "Bem-vindo(a) à API do projeto Backend-template!",
            "version": "v1",
            "links": {
                "products": "/api/v1/products/",
                "orders": "/api/v1/orders/",
            },
        }
    )


urlpatterns = [
    path("", RedirectView.as_view(url="/api/v1/", permanent=False)),
    path("admin/", admin.site.urls),

    # auth
    path("api-token-auth/", obtain_auth_token),

    # root da API
    path("api/v1/", api_root),

    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Redoc UI
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # apps
    path("api/v1/products/", include("products.urls")),
    path("api/v1/orders/", include("orders.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("api/v1/access/", include("access.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
