import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from ecommerce.apps.orders.models import Order
from ecommerce.apps.orders.serializers import (
    OrderItemSerializer,
    OrderReadSerializer,
    OrderWriteSerializer,
)

from ..factories import OrderFactory, OrderItemFactory, ProductFactory, UserFactory


@pytest.mark.django_db
def test_order_read_serializer():
    user = UserFactory()
    product = ProductFactory()
    order = OrderFactory(buyer=user)
    order_item = OrderItemFactory(order=order, product=product)

    serializer = OrderReadSerializer(instance=order)
    assert serializer.data["id"] == order.id
    assert serializer.data["buyer"] == order.buyer.get_full_name
    assert serializer.data["total_cost"] == order.total_cost
    assert len(serializer.data["order_items"]) == 1
    assert serializer.data["order_items"][0]["product_name"] == order_item.product.name
