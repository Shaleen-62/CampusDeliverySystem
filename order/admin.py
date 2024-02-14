from django.contrib import admin
from .models import Cart, Orders, OrderItems

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # list_display = ('id', 'username', 'food', 'quantity','restaurant')
    list_display = ('id', 'username', 'food', 'quantity')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    # list_display = ('id', 'username', 'total_amount', 'order_datetime', 'payment_mode', 'status', 'transaction_id', 'payment_gateway','restaurant')
    list_display = ('id', 'username', 'total_amount', 'order_datetime', 'payment_mode', 'status', 'transaction_id', 'payment_gateway')

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    # list_display = ('id', 'username', 'order', 'name', 'price', 'quantity', 'item_total','restaurant')
    list_display = ('id', 'username', 'order', 'name', 'price', 'quantity', 'item_total')
 