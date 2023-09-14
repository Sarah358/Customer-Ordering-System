from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Category, Product
from .serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for product categories.
    """

    queryset = Category.objects.all()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductReadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for reading products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProductWriteViewSet(viewsets.ModelViewSet):
    """
    Viewset for writing products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductWriteSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        # Check if the user is an admin
        if not request.user.is_staff:
            return Response(
                {"message": "You do not have permission to create products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Check if the user is an admin
        if not request.user.is_staff:
            return Response(
                {"message": "You do not have permission to update products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Check if the user is an admin
        if not request.user.is_staff:
            return Response(
                {"message": "You do not have permission to delete products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)
