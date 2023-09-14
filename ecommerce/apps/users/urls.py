from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'users'
