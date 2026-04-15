from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity', 'get_total_price']

    def get_total_price(self, obj):
        return f"TSH {obj.get_total_price():,.0f}"
    get_total_price.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'region', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'region', 'created_at']
    list_editable = ['status']
    search_fields = ['full_name', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    ordering = ['-created_at']
