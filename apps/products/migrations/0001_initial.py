from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('name_sw', models.CharField(blank=True, max_length=100, verbose_name='Name (Swahili)')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('description_sw', models.TextField(blank=True, verbose_name='Description (Swahili)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='Image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('name_sw', models.CharField(blank=True, max_length=200, verbose_name='Name (Swahili)')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('description_sw', models.TextField(blank=True, verbose_name='Description (Swahili)')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Price (TSH)')),
                ('unit', models.CharField(default='piece', help_text='e.g. piece, kg, tray (30 eggs), chick', max_length=50, verbose_name='Unit')),
                ('unit_sw', models.CharField(blank=True, max_length=50, verbose_name='Unit (Swahili)')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Main Image')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Image 2')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Image 3')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
                ('is_available', models.BooleanField(default=True, verbose_name='Available')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured on Homepage')),
                ('minimum_order', models.PositiveIntegerField(default=1, verbose_name='Minimum Order Quantity')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['-created_at'],
            },
        ),
    ]
