from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order, OrderItem
from .permissions import IsOrderItemPending, IsOrderPending
from .serializers import OrderItemSerializer, OrderReadSerializer, OrderWriteSerializer
from .tasks import send_order_confirmation_sms


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD order items that are associated with the current order id.
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    """
    This method overrides the default queryset for the viewset.
    It filters the queryset to only include OrderItem
    objects associated with a specific order, determined by
    the order_id from the URL
    """

    def get_queryset(self):
        res = super().get_queryset()
        order_id = self.kwargs.get('order_id')
        return res.filter(order__id=order_id)

    """
    This method is called when a new order item is created.
    It retrieves the associated order based on the order_id from the URL and
    then saves the order item with the associated order
    """

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        serializer.save(order=order)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes += [IsOrderItemPending]

        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD orders of a user
    """

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    # enable filtering by order status
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return OrderWriteSerializer

        return OrderReadSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user

        # Retrieve the "status" query parameter from the URL
        status_param = self.request.query_params.get('status')

        # Filter orders by status if the "status" query parameter is provided
        if status_param:
            res = res.filter(status=status_param)
        return res.filter(buyer=user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsOrderPending]

        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        order = self.get_object()

        if order.status == Order.COMPLETED:
            return Response(
                {"error": "This order has already been completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.status == Order.PLACED:
            return Response(
                {"error": "This order has already been placed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = Order.PLACED
        order.save()

        # trigger the task to send SMS
        send_order_confirmation_sms.delay(order.id)

        return Response(
            {
                "message": "Order placed successfully. You will receive a confirmation message shortly."
            },
            status=status.HTTP_200_OK,
        )
