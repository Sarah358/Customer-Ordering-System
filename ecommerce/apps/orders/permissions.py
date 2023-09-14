from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission

from .models import Order


class IsOrderPending(BasePermission):
    """
    Check the status of order is pending or completed before updating/deleting instance
    """

    message = _('Updating or deleting placed order is not allowed.')

    def has_object_permission(self, request, view, obj):
        if view.action in ('retrieve',):
            return True
        return obj.status == 'P'


class IsOrderItemPending(BasePermission):
    """
    Check the status of order is pending or completed before creating, updating and deleting order items
    """

    message = _('Creating, updating or deleting order items for a placed order is not allowed.')

    def has_permission(self, request, view):
        order_id = view.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        if view.action in ('list',):
            return True

        return order.status == 'P'

    def has_object_permission(self, request, view, obj):
        if view.action in ('retrieve',):
            return True
        return obj.order.status == 'P'
