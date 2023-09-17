from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from ecommerce.apps.orders.models import Order, OrderItem
from ecommerce.apps.orders.permissions import IsOrderItemPending, IsOrderPending
from tests.factories import OrderFactory, OrderItemFactory, ProductFactory, UserFactory


class OrderItemViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.order = OrderFactory()
        self.product = ProductFactory()
        self.order_item = OrderItemFactory(order=self.order, product=self.product)
        self.url = f'/api/v1/orders/{self.order.id}/order-items/'

    def test_create_order_item(self):
        self.product = ProductFactory()
        data = {
            'product': self.product.id,
            'quantity': 1,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format='json')

        if response.status_code != status.HTTP_201_CREATED:
            print(response.status_code)
            print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_item_permission(self):
        # Assuming you have implemented IsOrderItemPending correctly
        self.client.force_authenticate(user=self.user)
        self.order.status = 'C'  # Set order status to 'Completed'
        self.order.save()
        data = {
            'order': self.order.id,
            'product': self.product.id,
            'quantity': 1,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_order_item_pending_permission(self):
        # Create an order with status 'P'
        self.product = ProductFactory()
        order = OrderFactory()
        self.client.force_authenticate(user=self.user)
        data = {
            'order': order.id,
            'product': self.product.id,
            'quantity': 1,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try to update the order item with status 'C'
        order_item = OrderItem.objects.latest('id')
        order_item.order.status = 'C'
        order_item.order.save()
        data = {
            'quantity': 1,
        }
        response = self.client.patch(f'{self.url}{order_item.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.order = OrderFactory(buyer=self.user)
        self.url = '/api/v1/orders/'

    def test_create_order(self):
        self.product = ProductFactory()

        # Create order items data (replace with actual order items)
        order_items_data = [
            {
                'product': self.product.id,
                'quantity': 2,
            },
        ]

        data = {
            'buyer': self.user.id,
            'status': 'P',
            'order_items': order_items_data,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format='json')

        if response.status_code != status.HTTP_201_CREATED:
            print(response.status_code)
            print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_is_order_pending_permission(self):
        self.client.force_authenticate(user=self.user)
        self.order.status = 'C'  # Set order status to 'Completed'
        self.order.save()
        response = self.client.patch(
            f'{self.url}{self.order.id}/', data={'status': 'P'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_order_permission(self):
        # Test permission for updating an order status to 'P' when it's not allowed
        self.client.force_authenticate(user=self.user)
        self.order.status = 'C'  # Set order status to 'Completed'
        self.order.save()
        data = {
            'status': 'P',  # Try to update to 'P' status
        }
        response = self.client.patch(f'{self.url}{self.order.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_checkout_order(self):
        # Test checkout action when order status is 'P'
        self.client.force_authenticate(user=self.user)
        self.order.status = 'P'
        self.order.save()
        response = self.client.post(f'{self.url}{self.order.id}/checkout/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['message'],
            "Order placed successfully. You will receive a confirmation message shortly.",
        )

        # Test checkout action when order status is 'C' (already completed)
        self.order.status = 'C'  # Set order status to 'Completed'
        self.order.save()
        response = self.client.post(f'{self.url}{self.order.id}/checkout/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "This order has already been completed.")

        # Test checkout action when order status is 'Placed' (already placed)
        self.order.status = 'L'  # Set order status to 'Placed'
        self.order.save()
        response = self.client.post(f'{self.url}{self.order.id}/checkout/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "This order has already been placed.")
