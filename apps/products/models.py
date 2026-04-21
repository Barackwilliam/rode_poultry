from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    name_sw = models.CharField(_('Name (Swahili)'), max_length=100, blank=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(_('Description'), blank=True)
    description_sw = models.TextField(_('Description (Swahili)'), blank=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(_('Name'), max_length=200)
    name_sw = models.CharField(_('Name (Swahili)'), max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(_('Description'), blank=True)
    description_sw = models.TextField(_('Description (Swahili)'), blank=True)
    price = models.DecimalField(_('Price (TSH)'), max_digits=12, decimal_places=2)
    unit = models.CharField(_('Unit'), max_length=50, default='piece',
                            help_text='e.g. piece, kg, tray (30 eggs), chick')
    unit_sw = models.CharField(_('Unit (Swahili)'), max_length=50, blank=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    image2 = models.CharField(max_length=255, blank=True, null=True)
    image3 = models.CharField(max_length=255, blank=True, null=True)
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    is_available = models.BooleanField(_('Available'), default=True)
    is_featured = models.BooleanField(_('Featured on Homepage'), default=False)
    is_upcoming = models.BooleanField(_('Upcoming Product'), default=False,
                                      help_text='Inaonyesha kwenye sehemu ya "Inakuja Hivi Karibuni"')
    upcoming_date = models.DateField(_('Expected Arrival Date'), null=True, blank=True,
                                     help_text='Tarehe inayotarajiwa kufika (optional)')
    # Offer / Sale price
    offer_price = models.DecimalField(_('Offer Price (TSH)'), max_digits=12, decimal_places=2,
                                       null=True, blank=True, help_text='Acha wazi kama hakuna ofa')
    offer_label = models.CharField(_('Offer Label'), max_length=60, blank=True,
                                    help_text='e.g. "Flash Sale", "Wiki Hii Tu", "Punguzo la 20%"')
    offer_label_sw = models.CharField(_('Offer Label (Swahili)'), max_length=60, blank=True)
    minimum_order = models.PositiveIntegerField(_('Minimum Order Quantity'), default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_on_offer(self):
        return self.offer_price is not None and self.offer_price < self.price

    @property
    def discount_percent(self):
        if self.is_on_offer:
            return round((self.price - self.offer_price) / self.price * 100)
        return 0

    @property
    def display_price(self):
        """Returns offer_price if active, else normal price."""
        return self.offer_price if self.is_on_offer else self.price

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def get_name(self, lang='en'):
        if lang == 'sw' and self.name_sw:
            return self.name_sw
        return self.name

    def get_description(self, lang='en'):
        if lang == 'sw' and self.description_sw:
            return self.description_sw
        return self.description
    # Open Graph image (Facebook / WhatsApp preview)
    def get_og_image_url(self):
        if self.image:
            return f"https://ucarecdn.com/{self.image}/-/resize/1200x630/-/format/auto/"
        return ""

    # Optimized image for normal website usage
    def get_image_url(self):
        if self.image:
            return f"https://ucarecdn.com/{self.image}/-/format/jpg/-/quality/smart/"
        return ""
