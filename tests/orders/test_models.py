from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from ..factories import OrderFactory, OrderItemFactory, ProductFactory, UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_order_model():
    user = UserFactory()
    order = OrderFactory(buyer=user)
    assert str(order) == user.get_full_name
    assert order.total_cost == Decimal('0.00')  # No order items, so the total cost should be zero


@pytest.mark.django_db
def test_orderitem_model():
    product = ProductFactory()
    order = OrderFactory()
    order_item = OrderItemFactory(order=order, product=product, quantity=3)

    assert str(order_item) == order.buyer.get_full_name
    assert order_item.cost == product.price * order_item.quantity


@pytest.mark.django_db
def test_order_total_cost():
    user = UserFactory()
    order = OrderFactory(buyer=user)
    products = [ProductFactory() for _ in range(3)]

    for product in products:
        OrderItemFactory(order=order, product=product, quantity=2)

    expected_total_cost = sum(product.price * 2 for product in products)
    assert order.total_cost == expected_total_cost
