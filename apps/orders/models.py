from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('processing', _('Processing')),
        ('ready', _('Ready for Delivery')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    # Customer info
    full_name = models.CharField(_('Full Name'), max_length=200)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone Number'), max_length=20)
    address = models.TextField(_('Delivery Address'))
    region = models.CharField(_('Region'), max_length=100, default='Morogoro')
    notes = models.TextField(_('Order Notes'), blank=True)

    # Order meta
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(_('Payment Method'), max_length=50, default='Cash on Delivery')
    total_amount = models.DecimalField(_('Total Amount (TSH)'), max_digits=14, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} — {self.full_name}'

    def calculate_total(self):
        self.total_amount = sum(item.get_total_price() for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)  # snapshot
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}x {self.product_name}'

    def get_total_price(self):
        return self.price * self.quantity
