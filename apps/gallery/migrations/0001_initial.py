from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('name_sw', models.CharField(blank=True, max_length=100, verbose_name='Name (Swahili)')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Gallery Categories',
            },
        ),
        migrations.CreateModel(
            name='GalleryMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(
                    choices=[('image', 'Image'), ('youtube', 'YouTube Video')],
                    default='image',
                    max_length=10,
                    verbose_name='Media Type',
                )),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('title_sw', models.CharField(blank=True, max_length=200, verbose_name='Title (Swahili)')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('description_sw', models.TextField(blank=True, verbose_name='Description (Swahili)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery/', verbose_name='Image')),
                ('youtube_url', models.URLField(blank=True, help_text='Full YouTube URL e.g. https://www.youtube.com/watch?v=XXXXX', verbose_name='YouTube URL')),
                ('youtube_thumbnail', models.URLField(blank=True, verbose_name='YouTube Thumbnail URL')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Display Order')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gallery.gallerycategory')),
            ],
            options={
                'verbose_name': 'Gallery Media',
                'verbose_name_plural': 'Gallery Media',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
