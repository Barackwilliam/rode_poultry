from django.contrib import admin
from .models import Order, OrderItem, PromoCode


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity', 'get_total_price']

    def get_total_price(self, obj):
        return f"TSH {obj.get_total_price():,.0f}"
    get_total_price.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'region', 'total_amount', 'payment_method', 'payment_status', 'status', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'region', 'created_at']
    list_editable = ['status', 'payment_status']
    search_fields = ['full_name', 'phone', 'email', 'discount_code']
    readonly_fields = ['created_at', 'updated_at', 'subtotal', 'total_amount', 'deposit_amount', 'balance_due']
    inlines = [OrderItemInline]
    ordering = ['-created_at']


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'is_active', 'description']
    list_editable = ['is_active']
    search_fields = ['code']
