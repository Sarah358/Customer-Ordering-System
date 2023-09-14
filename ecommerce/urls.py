from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('ecommerce.base_urls')),
    path("api/v1/auth/", include('djoser.urls')),
    path("api/v1/auth/", include('djoser.urls.jwt')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
]

admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome To The Ecommerce Portal"
