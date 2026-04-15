from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='Full Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('address', models.TextField(verbose_name='Delivery Address')),
                ('region', models.CharField(default='Morogoro', max_length=100, verbose_name='Region')),
                ('notes', models.TextField(blank=True, verbose_name='Order Notes')),
                ('status', models.CharField(
                    choices=[
                        ('pending', 'Pending'),
                        ('confirmed', 'Confirmed'),
                        ('processing', 'Processing'),
                        ('ready', 'Ready for Delivery'),
                        ('delivered', 'Delivered'),
                        ('cancelled', 'Cancelled'),
                    ],
                    default='pending',
                    max_length=20,
                    verbose_name='Status',
                )),
                ('payment_method', models.CharField(default='Cash on Delivery', max_length=50, verbose_name='Payment Method')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=14, verbose_name='Total Amount (TSH)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
        ),
    ]
