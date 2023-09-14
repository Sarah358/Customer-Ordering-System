from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'status', 'ref', 'created_at', 'updated_at', 'total_cost')
    list_filter = ('status', 'buyer')
    search_fields = ('ref', 'buyer__username', 'buyer__first_name', 'buyer__last_name')
    list_per_page = 20


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
