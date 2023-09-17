# test_tasks.py
from unittest.mock import Mock, patch

import pytest
from django.conf import settings

from ecommerce.apps.orders.models import Order, OrderItem
from ecommerce.apps.orders.tasks import send_order_confirmation_sms
from ecommerce.apps.products.models import Product
from ecommerce.apps.users.models import User


@pytest.mark.django_db
@patch('ecommerce.apps.orders.tasks.Client')
def test_send_order_confirmation_sms(mocker):
    product = Product.objects.create(name='Test Product', stock=10, price=20)

    buyer = User.objects.create(
        username="testbuyer",
        first_name="John",
        last_name="Doe",
        phone_number="+254799757242",
        email="john@example.com",
        password="testpassword",
    )

    # Create an Order without associating OrderItems yet
    order = Order.objects.create(
        buyer=buyer,
        status=Order.PENDING,
        ref='test_ref',
    )

    # Create OrderItems
    order_item = OrderItem.objects.create(order=order, product=product, quantity=2)

    # Associate OrderItem with the Order
    order.order_items.add(order_item)

    # Replace Twilio client with a mock
    mock_twilio_client_instance = Mock()
    mock_twilio_client = Mock(return_value=mock_twilio_client_instance)

    with patch('ecommerce.apps.orders.tasks.Client', mock_twilio_client):
        # Call the Celery task
        send_order_confirmation_sms(order.id)

    # Assert that the Twilio client was initialized correctly
    mock_twilio_client.assert_called_once_with(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
    )

    # Assert that the Twilio message was created and sent correctly
    mock_twilio_client_instance.messages.create.assert_called_once_with(
        body=f"Thank you for your order with us! Your order reference code is {order.ref}. Total cost: {order.total_cost}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to='+254799757242',
    )
