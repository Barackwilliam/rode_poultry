from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.products.models import Product


class PromoCode(models.Model):
    code = models.CharField(_('Code'), max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(_('Discount (%)'), default=10)
    is_active = models.BooleanField(_('Active'), default=True)
    description = models.CharField(_('Description'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('Promo Code')
        verbose_name_plural = _('Promo Codes')

    def __str__(self):
        return f'{self.code} — {self.discount_percent}%'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('processing', _('Processing')),
        ('ready', _('Ready for Delivery')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('mpesa', _('M-Pesa')),
        ('tigopesa', _('Tigo Pesa')),
        ('airtelmoney', _('Airtel Money')),
        ('halopesa', _('HaloPesa')),
        ('cod', _('Cash on Delivery')),
        ('deposit', _('70/30 Deposit — Pay 30% on delivery')),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', _('Unpaid')),
        ('deposit_paid', _('Deposit Paid (70%)')),
        ('paid', _('Paid')),
    ]

    # Customer info
    full_name = models.CharField(_('Full Name'), max_length=200)
    email = models.EmailField(_('Email'), blank=True)
    phone = models.CharField(_('Phone Number'), max_length=20)
    address = models.TextField(_('Delivery Address'))
    region = models.CharField(_('Region'), max_length=100, default='Morogoro')
    notes = models.TextField(_('Order Notes'), blank=True)

    # Order meta
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(_('Payment Method'), max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(_('Payment Status'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    # Pricing
    subtotal = models.DecimalField(_('Subtotal (TSH)'), max_digits=14, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(_('Delivery Fee (TSH)'), max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('Discount (TSH)'), max_digits=10, decimal_places=2, default=0)
    discount_code = models.CharField(_('Promo Code'), max_length=50, blank=True)
    total_amount = models.DecimalField(_('Total Amount (TSH)'), max_digits=14, decimal_places=2, default=0)

    # Deposit tracking (for 70/30 option)
    deposit_amount = models.DecimalField(_('Deposit Paid (TSH)'), max_digits=14, decimal_places=2, default=0)
    balance_due = models.DecimalField(_('Balance Due on Delivery (TSH)'), max_digits=14, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} — {self.full_name}'

    def calculate_total(self):
        self.subtotal = sum(item.get_total_price() for item in self.items.all())
        # Delivery = nusu ya gharama ya kawaida (tunaweka delivery_fee manually au formula)
        self.total_amount = self.subtotal + self.delivery_fee - self.discount_amount
        if self.payment_method == 'deposit':
            self.deposit_amount = round(self.total_amount * 70 / 100, 2)
            self.balance_due = self.total_amount - self.deposit_amount
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

