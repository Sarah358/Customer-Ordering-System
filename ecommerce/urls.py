from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('ecommerce.base_urls')),
    path("api/v1/auth/", include('djoser.urls')),
    path("api/v1/auth/", include('djoser.urls.jwt')),
    path(
        'swagger(?P<format>\.json|\.yaml)',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome To The Ecommerce Portal"
