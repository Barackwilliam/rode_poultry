from django.db import models
from django.utils.translation import gettext_lazy as _


class GalleryCategory(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    name_sw = models.CharField(_('Name (Swahili)'), max_length=100, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Gallery Categories'

    def __str__(self):
        return self.name


class GalleryMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', _('Image')),
        ('youtube', _('YouTube Video')),
    ]

    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True)
    media_type = models.CharField(_('Media Type'), max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    title = models.CharField(_('Title'), max_length=200)
    title_sw = models.CharField(_('Title (Swahili)'), max_length=200, blank=True)
    description = models.TextField(_('Description'), blank=True)
    description_sw = models.TextField(_('Description (Swahili)'), blank=True)

    # For images
    image = models.CharField(max_length=255, blank=True, null=True)

    # For YouTube videos
    youtube_url = models.URLField(_('YouTube URL'), blank=True,
                                  help_text='Full YouTube URL e.g. https://www.youtube.com/watch?v=XXXXX')
    youtube_thumbnail = models.URLField(_('YouTube Thumbnail URL'), blank=True)

    is_active = models.BooleanField(_('Active'), default=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Gallery Media')
        verbose_name_plural = _('Gallery Media')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_youtube_embed_url(self):
        """Convert YouTube watch URL to embed URL."""
        if not self.youtube_url:
            return ''
        import re
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return f'https://www.youtube.com/embed/{match.group(1)}'
        return self.youtube_url

    def get_youtube_id(self):
        import re
        if not self.youtube_url:
            return ''
        match = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', self.youtube_url)
        return match.group(1) if match else ''
