# from rest_framework import urlpatterns

from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path("users/", include("ecommerce.apps.users.urls", namespace="users")),
    path("profile/", include("ecommerce.apps.profiles.urls", namespace="profiles")),
    # path("products/", include("ecommerce.apps.products.urls", namespace="products")),
    # path("orders/", include("ecommerce.apps.orders.urls", namespace="orders")),
]

urlpatterns += router.urls
